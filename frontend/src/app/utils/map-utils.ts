/**
 * Creates LatLng Literal Object from Lat and Lng Number
 * @param lat
 * @param lng
 */
import LatLngLiteral = google.maps.LatLngLiteral;

export function createLatLngLiteral(lat: number, lng: number): LatLngLiteral {
  return {
    lat: lat,
    lng: lng
  } as LatLngLiteral
}
