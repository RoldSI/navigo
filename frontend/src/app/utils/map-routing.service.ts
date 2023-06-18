import {Injectable, NgZone} from '@angular/core';
import {combineLatest, from, map, Observable, Subject, switchMap} from "rxjs";
import {MapDirectionsResponse, MapGeocoder, MapGeocoderResponse} from "@angular/google-maps";
import {createLatLngLiteral} from "./map-utils";
import {ApiService} from "./api.service";
import LatLngLiteral = google.maps.LatLngLiteral;
import TravelMode = google.maps.TravelMode;

export type RouteDirectionResult = {
  directionsResult: google.maps.DirectionsResult,
  mode: google.maps.TravelMode,
  distance: string;
  duration: string;
  efficiency: number;
}


@Injectable({
  providedIn: 'root'
})
export class MapRoutingService {
  private routeSubject: Subject<RouteDirectionResult[]>;
  public route$: Observable<RouteDirectionResult[]>;

  public startLocation: string = "";
  public endLocation: string = "";

  private _directionsService: google.maps.DirectionsService | undefined;

  constructor(private readonly _ngZone: NgZone, private readonly geocoder: MapGeocoder, private apiService: ApiService) {
    this.routeSubject = new Subject<RouteDirectionResult[]>();
    this.route$ = this.routeSubject.asObservable();
  };

  createDirectionRequest(source: string, dest: string): void {
    this.startLocation = source;
    this.endLocation = dest;
    this.apiService.getRoutes({from: source, to: dest}).subscribe((res) => {
      console.log(res);
      const obj: RouteDirectionResult[] = []
      for (const key in res) {
        if (res.hasOwnProperty(key)) {
          const value = res[key];
          const transportMode = value.directionsResult.available_travel_modes
          // if(!!(transportMode) || transportMode[0]) return;
          obj.push({
            ...value,
            mode: (transportMode && transportMode[0]) ? transportMode[0] : TravelMode.BICYCLING,
          })
        }
      }
      this.routeSubject.next(obj)
    });
  }

  /**
   * Use it like "this.directionsResults$ = service.createDirectionRequest(...).pipe(map(response => response.result));"
   * @param start
   * @param destination
   * @param travelMode
   */

  createTmpRequest(start: LatLngLiteral, destination: LatLngLiteral, travelMode: google.maps.TravelMode): Observable<undefined | google.maps.DirectionsResult>;
  createTmpRequest(start: string, destination: string, travelMode: google.maps.TravelMode): Observable<undefined | google.maps.DirectionsResult>;
  createTmpRequest(start: LatLngLiteral | string, destination: LatLngLiteral | string, travelMode: google.maps.TravelMode): Observable<undefined | google.maps.DirectionsResult> {
    const start$: Observable<LatLngLiteral> = (typeof start === 'string') ? this.addressToLatLng(start) : from([start]);
    const destination$: Observable<LatLngLiteral> = (typeof destination === 'string') ? this.addressToLatLng(destination) : from([destination]);

    return combineLatest([start$, destination$]).pipe(
      switchMap(([startLatLng, destinationLatLng]: LatLngLiteral[]) => {
        const request: google.maps.DirectionsRequest = {
          origin: startLatLng as LatLngLiteral,
          destination: destinationLatLng as LatLngLiteral,
          travelMode: travelMode as google.maps.TravelMode
        };
        return this.route(request).pipe(map((res: MapDirectionsResponse) => {
          if (res.status !== google.maps.DirectionsStatus.OK) {
            console.warn("Route from  ", origin, " to ", destination, " couldn't be resolved!");
            return undefined;
          } else if (res.result?.routes.length === 0) {
            console.warn("Route from  ", origin, " to ", destination, " couldn't be find!");
            return undefined;
          } else {
            console.log("Route Found: ", res.result);
            return res.result
            // console.log(res.result?.routes[0]);
            // return res.result?.routes[0];
          }
        }));
      })
    );
  }

  addressToLatLng(address: string): Observable<google.maps.LatLngLiteral>;
  addressToLatLng(address: google.maps.GeocoderRequest): Observable<MapGeocoderResponse>;
  addressToLatLng(address: string | google.maps.GeocoderRequest): Observable<google.maps.LatLngLiteral | MapGeocoderResponse> {
    let tmp: Observable<MapGeocoderResponse>;
    if (typeof address === "string") {
      tmp = this.geocoder.geocode({
        address: address
      })
    } else {
      tmp = this.geocoder.geocode(address);
    }

    return tmp.pipe(
      map((res: MapGeocoderResponse) => {
        if (res.status !== google.maps.GeocoderStatus.OK) {
          console.warn("Address ", address, " couldn't be resolved!");
          return createLatLngLiteral(0, 0);
        } else {
          const tmp = res.results[0].geometry.location;
          return createLatLngLiteral(tmp.lat(), tmp.lng());
        }
      })
    );
  }

  /**
   * See
   * developers.google.com/maps/documentation/javascript/reference/directions
   * #DirectionsService.route
   */
  route(request: google.maps.DirectionsRequest): Observable<MapDirectionsResponse> {
    return new Observable(observer => {
      // Initialize the `DirectionsService` lazily since the Google Maps API may
      // not have been loaded when the provider is instantiated.
      if (!this._directionsService) {
        this._directionsService = new google.maps.DirectionsService();
      }

      this._directionsService.route(request, (result, status) => {
        this._ngZone.run(() => {
          observer.next({result: result || undefined, status});
          observer.complete();
        });
      });
    });
  }
}
