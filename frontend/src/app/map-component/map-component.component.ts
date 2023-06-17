import {Component, ViewChild} from '@angular/core';
import {MapGeocoderResponse, MapInfoWindow, MapMarker} from "@angular/google-maps";
import {MapRoutingService} from "../utils/map-routing.service";

declare const google: any;

type Marker = {
  options: google.maps.MarkerOptions,
  position: google.maps.LatLngLiteral
}

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
  center: google.maps.LatLngLiteral = {lat: 24, lng: 12};

  /**
   * Default Map Zoom
   */
  zoom = 4;

  /**
   * Display
   */
  display: google.maps.LatLngLiteral | undefined;

  markers: Marker[] = [];
  // markerOptions: google.maps.MarkerOptions = {draggable: false};
  // markerPositions: google.maps.LatLngLiteral[] = [];

  createDefaultMarker(pos: google.maps.LatLngLiteral): Marker {
    return this.createMarker(pos,
      {
        draggable: false
      })
  }

  createMarker(pos: google.maps.LatLngLiteral, options: google.maps.MarkerOptions): Marker {
    return {
      position: pos,
      options: options
    }
  }

  constructor(private readonly mapRoutingService: MapRoutingService) {
    this.mapRoutingService.addressStringToLatLang('Am Großmarkt 10, 76137 Karlsruhe')
      .subscribe((results: MapGeocoderResponse) => {
        const res = results.results[0];
        this.center = {
          lat: res.geometry.location.lat(),
          lng: res.geometry.location.lng()
        };
        this.zoom = 15;
        this.markers.push(this.createDefaultMarker(this.center));

        // this.center = results[0];
      });
  }

  ngOnInit(): void {

  }

  moveMap(event: google.maps.MapMouseEvent) {
    console.log("Move Map Event: ", event);
  }

  move(event: google.maps.MapMouseEvent) {
    console.log("Move Event: ", event);
  }

  openInfoWindow(marker: MapMarker) {
    this.infoWindow?.open(marker);
  }

  addMarker(event: google.maps.MapMouseEvent) {
    if (event.latLng) {
      this.markers.push(this.createDefaultMarker(event.latLng.toJSON()));
    }
  }
}
