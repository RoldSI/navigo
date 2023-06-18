import {Injectable} from "@angular/core";

@Injectable({
  providedIn: 'root'
})
export class MapService {
  private colors: Record<google.maps.TravelMode, string> = {
    DRIVING: '#FF0000',  // Red
    WALKING: '#00FF00',  // Green
    BICYCLING: '#0000FF',  // Blue
    TRANSIT: '#FFA500'  // Orange
  };

  getSettingsByMode(mode: google.maps.TravelMode): google.maps.PolylineOptions {
    const color = this.colors[mode];

    return {
      strokeColor: color,
      strokeOpacity: 0.8,
      strokeWeight: 3
    };
  }
}
