import requests
import polyline
from dotenv import dotenv_values


env_vars = dotenv_values(".env")
GMAPS_KEY = env_vars["GMAPS_KEY"]

def calculate_route_gmaps(start, end, mode):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode={mode}&key={GMAPS_KEY}"
    gmaps_response = requests.get(url).json()

    if gmaps_response["status"] == "OK":
        waypoints = gmaps_response["geocoded_waypoints"]
        routes = gmaps_response["routes"]
        route = gmaps_response["routes"][0]
        distance = route["legs"][0]["distance"]["value"]
        duration = route["legs"][0]["duration"]["value"]
        
        return distance, duration, waypoints, routes
    else:
        print("GMAPS FAILED")
        return None, gmaps_response, None, None


def get_maneuvers(routes):
    # routes_ct = len(gmaps_response['routes']) 
    # print(f"{routes_ct=}")
    # assert routes_ct == 1

    route_0 = routes[0]
    maneuvers = []
    
    # print(f"{len(route_0['legs'])=}")
    for leg in route_0['legs']:
        # print(f"{len(leg['steps'])=}")
        for step in leg['steps']:
            # print(step)
            try:
                # len_steps_in_step = len(step['steps'])
                # print(f"{len_steps_in_step=}")
                for steps_in_step in step['steps']:
                    try:
                        maneuver = steps_in_step['maneuver']
                        # print(f"{maneuver=}")
                        maneuvers.append(maneuver)
                    except:
                        pass
                    # print(f"{len(maneuvers)=}")
            except:
                # print("NO STEPS IN 'STEP'")
                try:

                    weird_maneuver = step['maneuver']
                    # print(f"{step['maneuver']=}")
                    maneuvers.append(weird_maneuver)
                    # print("HANDLE THIS!!! \n'\n HANDLE WEIRD MANEUVERS!!")

                except:
                    # print("BUT THERE ARE NO MANEUVERS IN THIS STEP ANYWAYS")
                    pass
    return maneuvers
