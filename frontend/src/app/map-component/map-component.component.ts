import {Component, ViewChild} from '@angular/core';
import {GoogleMap, MapInfoWindow, MapMarker} from "@angular/google-maps";
import {MapRoutingService, RouteDirectionResult} from "../utils/map-routing.service";
import {MarkerBuilder, MarkerType} from "../utils/marker-builder";
import {decode} from "polyline";
import {createLatLngLiteral} from "../utils/map-utils";
import {MapService} from "../utils/map.service";
import DirectionsStep = google.maps.DirectionsStep;
import LatLng = google.maps.LatLng;
import LatLngBounds = google.maps.LatLngBounds;


@Component({
  selector: 'map-component',
  templateUrl: './map-component.component.html',
  styleUrls: ['./map-component.component.scss']
})
export class MapComponentComponent {
  @ViewChild(GoogleMap) map: GoogleMap | undefined;
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

  constructor(private readonly mapRoutingService: MapRoutingService, private readonly mapService: MapService) {
  }

  private getDefaultMarkers() {
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
  }

  routes: {
    directions: LatLng[],
    options: google.maps.PolylineOptions
  }[] = [];
  startLocation: { lat: number, lng: number } | undefined;
  destinationLocation: { lat: number, lng: number } | undefined;
  bounds: any;

  ngOnInit(): void {
    this.mapRoutingService.route$.subscribe((res: RouteDirectionResult[]) => {
      this.routes = [];
      this.markers = [];
      this.getDefaultMarkers();

      res.forEach((r: any) => {
        this.startLocation = r.directionsResult.routes[0].legs[0].start_location;
        this.destinationLocation = r.directionsResult.routes[0].legs[0].end_location;

        // Set Bounds
        this.bounds = new LatLngBounds({
          north: r.directionsResult.routes[0].bounds.northeast.lat,
          east: r.directionsResult.routes[0].bounds.northeast.lng,
          south: r.directionsResult.routes[0].bounds.southwest.lat,
          west: r.directionsResult.routes[0].bounds.southwest.lng
        })

        // Set Directions
        let dirs: any[] = []
        r.directionsResult.routes[0].legs[0].steps.forEach((step: DirectionsStep) => {
          decode(step.polyline?.points || "").forEach((p: number[]) => {
            dirs.push(new LatLng(createLatLngLiteral(p[0], p[1])))
          })
        });


        this.routes.push({
          directions: dirs,
          options: this.mapService.getSettingsByMode(r.mode)
        });
      })

      // Create Markers for Start and End
      if (this.startLocation)
        this.markers.push(new MarkerBuilder().setDefaultIconSymbol(MarkerType.Default).setPosition(this.startLocation).buildMarker());
      if (this.destinationLocation)
        this.markers.push(new MarkerBuilder().setDefaultIconSymbol(MarkerType.End).setPosition(this.destinationLocation).buildMarker());

      if (!this.map || !this.bounds) return;
      this.map.fitBounds(this.bounds);
    })
  }

  getSettingsByMode(mode: google.maps.TravelMode): google.maps.DirectionsRendererOptions {

    return {
      suppressMarkers: true,
      polylineOptions: {
        strokeColor: '#5cb85c',
      }
    }
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
