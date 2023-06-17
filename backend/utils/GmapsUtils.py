import requests
import polyline
from dotenv import dotenv_values


env_vars = dotenv_values(".env")
GMAPS_KEY = env_vars["GMAPS_KEY"]

def calculate_route_gmaps(start, end, mode):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode={mode}&key={GMAPS_KEY}"
    gmaps_response = requests.get(url).json()
    if gmaps_response["status"] == "OK":
        route = gmaps_response["routes"][0]
        distance = route["legs"][0]["distance"]["value"]
        duration = route["legs"][0]["duration"]["value"]
        

        polyline_points = route["overview_polyline"]["points"]
        decoded_points = polyline.decode(polyline_points)
        return decoded_points, gmaps_response, distance, duration
    else:
        print("GMAPS FAILED")
        return None, gmaps_response, None, None
