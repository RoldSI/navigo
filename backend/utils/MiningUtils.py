
from GmapsUtils import calculate_route_gmaps
def predictAndDescribeClimate(distance, duration):
    print(f"{distance=} {duration=}")



if __name__ == "__main__":
    decoded_points, gmaps_response, distance, duration = calculate_route_gmaps("Berlin%20Hauptbahnhof", "Karlsruhe%20Hauptbahnhof", 
                          "public")
    if decoded_points: # meaning gmaps did return some OK response
        predictAndDescribeClimate(distance, duration)


