import {Injectable, NgZone} from '@angular/core';
import {Observable} from "rxjs";
import {MapDirectionsResponse, MapGeocoder, MapGeocoderResponse} from "@angular/google-maps";
import LatLngLiteral = google.maps.LatLngLiteral;

@Injectable({
  providedIn: 'root'
})
export class MapRoutingService {
  private _directionsService: google.maps.DirectionsService | undefined;

  constructor(private readonly _ngZone: NgZone, private readonly geocoder: MapGeocoder) {
  }

  createLatLngLiteral(lat: number, lng: number): LatLngLiteral {
    return {
      lat: lat,
      lng: lng
    } as LatLngLiteral
  }

  /**
   * Use it like "this.directionsResults$ = service.createDirectionRequest(...).pipe(map(response => response.result));"
   * @param start
   * @param destination
   * @param travelMode
   */
  createDirectionRequest(start: LatLngLiteral,
                         destination: LatLngLiteral,
                         travelMode: google.maps.TravelMode): Observable<MapDirectionsResponse> {
    return this.route(
      {
        destination: destination,
        origin: start,
        travelMode: travelMode
      });
  }

  addressObjToLatLang(addr: google.maps.GeocoderRequest): Observable<MapGeocoderResponse> {
    return this.geocoder.geocode(addr);
  }

  addressStringToLatLang(address: string): Observable<MapGeocoderResponse> {
    return this.geocoder.geocode({
      address: address
    })
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
