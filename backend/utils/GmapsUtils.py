# Import required libraries
import requests
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values(".env")

# Retrieve the Google Maps API Key from environment variables
GMAPS_KEY = env_vars["GMAPS_KEY"]


# Function to calculate route between two points using Google Maps API
def calculate_route_gmaps(start, end, mode):
    # Define the API request URL with required parameters
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode={mode}&key={GMAPS_KEY}"

    # Send GET request to the API and parse the response as JSON
    gmaps_response = requests.get(url).json()

    # Check if the response status is 'OK'
    if gmaps_response["status"] == "OK":
        # Extract waypoints and routes from the response
        waypoints = gmaps_response["geocoded_waypoints"]
        routes = gmaps_response["routes"]

        # Extract the first route
        route = gmaps_response["routes"][0]

        # Extract distance and duration from the first leg of the first route
        distance = route["legs"][0]["distance"]["value"]
        duration = route["legs"][0]["duration"]["value"]

        # Return distance, duration, waypoints and routes
        return distance, duration, waypoints, routes
    else:
        # Print error message if the response status is not 'OK'
        print("GMAPS FAILED")
        # Return None for distance, duration and routes, but the response for debugging
        return None, gmaps_response, None, None


# Function to get maneuvers from the given routes
def get_maneuvers(routes):
    # Extract the first route
    route_0 = routes[0]

    # Initialize list to store maneuvers
    maneuvers = []

    # Iterate over each leg in the route
    for leg in route_0['legs']:
        # Iterate over each step in the leg
        for step in leg['steps']:
            # Try to find nested steps in the current step
            try:
                for steps_in_step in step['steps']:
                    # Try to extract maneuver from the nested step
                    try:
                        maneuver = steps_in_step['maneuver']
                        # Add the maneuver to the list
                        maneuvers.append(maneuver)
                    except:
                        # Pass if there's no maneuver in the nested step
                        pass
            except:
                # If there are no nested steps, try to extract maneuver from the current step
                try:
                    weird_maneuver = step['maneuver']
                    # Add the maneuver to the list
                    maneuvers.append(weird_maneuver)
                except:
                    # Pass if there's no maneuver in the current step
                    pass
    # Return the list of maneuvers
    return maneuvers
