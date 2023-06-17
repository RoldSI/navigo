import { Component } from '@angular/core';

declare const google: any;

@Component({
  selector: 'map-component',
  templateUrl: './map-component.component.html',
  styleUrls: ['./map-component.component.scss']
})
export class MapComponentComponent {
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

  ngOnInit(): void {
  }

  moveMap(event: google.maps.MapMouseEvent) {
    console.log("Move Map Event: ", event);
  }

  move(event: google.maps.MapMouseEvent) {
    console.log("Move Event: ", event);
  }
}
