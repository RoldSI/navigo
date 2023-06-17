
from GmapsUtils import calculate_route_gmaps
import pprint
import sys
import os
def predictAndDescribeClimate(distance, duration):
    print(f"{distance=} {duration=}")




if __name__ == "__main__":
    decoded_points, gmaps_response, distance, duration = calculate_route_gmaps("Berlin%20Hauptbahnhof", "Karlsruhe%20Hauptbahnhof", 
                          "public")
    

    # Open the file in write mode
    file_path = './documents/gmaps_response.txt' 
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        # Redirect the output to the file
        sys.stdout = file

        # Use pprint.pprint() to print the string_data
        pprint.pprint(gmaps_response)

    # Reset the stdout to the default value (console)
    sys.stdout = sys.__stdout__


    if decoded_points: # meaning gmaps did return some OK response
        predictAndDescribeClimate(distance, duration)

