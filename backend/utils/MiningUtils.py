
from GmapsUtils import calculate_route_gmaps, get_maneuvers
import pprint
import sys
import os
def predictAndDescribeClimate(mode, distance, duration, maneuvers):
    # pdc stands for predict describe climate
    pdc = {}
    if mode == "car":
        print(f"{distance=} {duration=} {mode=} {maneuvers=}")
        # A typical value for CO2 emission per kilometer for a diesel-powered bus is around 120-150 grams of CO2 per kilometer (gCO2/km).
        # also 0.12-0.15 grams per meter
        # for each kilometer driven, turning right or left would result in an additional 5% of CO2 emissions.


    elif mode == "transit" :
        pass


    else:
        raise NotImplementedError
    return pdc
    

if __name__ == "__main__":

    # mode = "walking"
    mode = "transit"
    # mode = "car"

    decoded_points, gmaps_response, distance, duration = calculate_route_gmaps("London", "Karlsruhe%20Hauptbahnhof", mode)

    maneuvers = get_maneuvers(gmaps_response)
    



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
        predictAndDescribeClimate(mode, distance, duration, maneuvers)
