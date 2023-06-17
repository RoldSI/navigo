import {Component, ViewChild} from '@angular/core';
import {MapInfoWindow, MapMarker} from "@angular/google-maps";
import {MapRoutingService, RouteDirectionResult} from "../utils/map-routing.service";
import {MarkerBuilder, MarkerType} from "../utils/marker-builder";


@Component({
  selector: 'map-component',
  templateUrl: './map-component.component.html',
  styleUrls: ['./map-component.component.scss']
})
export class MapComponentComponent {
  @ViewChild(MapInfoWindow) infoWindow: MapInfoWindow | undefined;

  /**
   * Center of the Map
   */
  center: google.maps.LatLngLiteral = {
    lat: 51.10866477980172,
    lng: 10.49393043114157
  }

  /**
   * Default Map Zoom
   */
  zoom = 6;

  /**
   * Display
   */
  display: google.maps.LatLngLiteral | undefined;

  markers: google.maps.MarkerOptions[] = [];
  // markerOptions: google.maps.MarkerOptions = {draggable: false};
  // markerPositions: google.maps.LatLngLiteral[] = [];

  private readonly MSG_ADDRESS: string = "Am Großmarkt 10, 76137 Karlsruhe";
  private readonly HOTEL_ADDRESS: string = "Zimmerstraße 8, 76137 Karlsruhe";

  constructor(private readonly mapRoutingService: MapRoutingService) {
    // Create Favorite-Marker for the MSG-Address
    this.mapRoutingService.addressToLatLng(this.MSG_ADDRESS)
      .subscribe((res: google.maps.LatLngLiteral) => {
        this.markers.push(new MarkerBuilder().setDefaultIconSymbol(MarkerType.Favorite).setPosition(res).buildMarker());
      });

    // Create Information-Marker for the Hotel Address
    this.mapRoutingService.addressToLatLng(this.HOTEL_ADDRESS)
      .subscribe((res: google.maps.LatLngLiteral) => {
        this.markers.push(new MarkerBuilder().setDefaultIconSymbol(MarkerType.Information).setPosition(res).buildMarker());
      });
    /*
        this.mapRoutingService.createDirectionRequest(this.HOTEL_ADDRESS,
          this.MSG_ADDRESS,
          google.maps.TravelMode.DRIVING)
          .subscribe((res: google.maps.DirectionsResult | undefined) => {
            if (res === undefined) return;
            // this.res = res;
          })

        this.bicycleRes$ = this.mapRoutingService.createDirectionRequest(this.HOTEL_ADDRESS,
          this.MSG_ADDRESS,
          google.maps.TravelMode.BICYCLING);

        this.carRes$ = this.mapRoutingService.createDirectionRequest(this.HOTEL_ADDRESS,
          this.MSG_ADDRESS,
          google.maps.TravelMode.DRIVING);

        this.transitRes$ = this.mapRoutingService.createDirectionRequest(this.HOTEL_ADDRESS,
          this.MSG_ADDRESS,
          google.maps.TravelMode.TRANSIT);*/
  }

  routes: google.maps.DirectionsResult[] = [];


  opts: google.maps.DirectionsRendererOptions = {
    polylineOptions: {
      strokeColor: "red",
    }
  }


  ngOnInit(): void {
    this.mapRoutingService.createTmpRequest("Karlsruhe HBF", "Durlach Bahnhof", google.maps.TravelMode.WALKING).subscribe((res) => {
      console.log("RES: ", res)
    });

    this.mapRoutingService.route$.subscribe((res: RouteDirectionResult[]) => {
      res.forEach((r: RouteDirectionResult) => {
        const newRoutes:  google.maps.DirectionsRoute[] = []
        r.directionsResult.routes.forEach((route: google.maps.DirectionsRoute) => {
          console.log(route);

          // @ts-ignore
          route.bounds.north = route.bounds.northeast.lat;
          // @ts-ignore
          route.bounds.east = route.bounds.northeast.lng;
          // @ts-ignore
          route.bounds.sout = route.bounds.southwest.lat;
          // @ts-ignore
          route.bounds.west = route.bounds.southwest.lng;
          newRoutes.push(route);
        })
        r.directionsResult.routes = newRoutes;
        console.log(r.directionsResult);
        this.routes.push(r.directionsResult);
      })
    })
  }

  moveMap(event: google.maps.MapMouseEvent) {
    // console.log("Move Map Event: ", event);
  }

  move(event: google.maps.MapMouseEvent) {
    // console.log("Move Event: ", event);
    // console.log(event.latLng?.lat())
    // console.log(event.latLng?.lng())
  }

  openInfoWindow(marker: MapMarker) {
    this.infoWindow?.open(marker);
  }

  addMarker(event: google.maps.MapMouseEvent) {
    if (event.latLng) {
      this.markers.push(new MarkerBuilder()
        .setDefaultIconSymbol(MarkerType.Default)
        .setPosition(event.latLng.toJSON()).buildMarker());
    }
  }
}
