# Import necessary modules and libraries
from flask import Flask, jsonify, request
import firebase_admin
from flask_cors import CORS
from firebase_admin import credentials, auth, firestore
import openai
from utils import GmapsUtils
from transport_co2 import Mode  # https://pypi.org/project/transport-co2/
from dotenv import dotenv_values
import urllib
import requests
import json

# Import API-keys from .env file
env_vars = dotenv_values(".env")
OPENAI_API_KEY = env_vars["OPENAI_API_KEY"]
GMAPS_KEY = env_vars["GMAPS_KEY"]
openai.api_key = OPENAI_API_KEY

# Set up firebase for authentication and database
cred = credentials.Certificate('firebaseCredentials.json')
firebaseApp = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes
favorites = []


# Utility function to authenticate/validate a user based on some provided token with 
def authenticate_user(bearer_token):
    # Catch case of None token
    if bearer_token is None:
        return None
    try:
        # Validate token with firebase
        decoded_token = auth.verify_id_token(bearer_token)
        uid = decoded_token['uid']
        # return the user id for identification of the user
        return uid
    except Exception as e:
        # Authentication failed: return None for according handling
        return None


# For a logged-in user, add favorite locations
@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    # Do user authentication based on bearer token
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return jsonify({"error": "authentication failed"}), 401
    # Load user favorites from database
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    # Load new favorites from the request
    new_favorites = request.json['input']
    # Add new favorites to the database object
    for favorite in new_favorites:
        # Skip the favorite if already exists to avoid doubled favorites
        if favorite not in user_favorites_list:
            user_favorites_list.append(favorite)
            print(f"{favorite} added to favorites")
        else:
            print(f"{favorite} already in favorites")
    # Store the database object back to the database
    user_favorites_doc_ref.set({"favorites": user_favorites_list})
    return jsonify({"message": "Provided favorites added successfully"}), 200


# For a logged-in user, remove a location from favorites
@app.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    # User authentication
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return jsonify({"message": "authentication failed"}), 401
    # Get the user favorites from the database
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    # Get the to be removed favorites from the request
    remove_favorites = request.json['input']
    # Remove those favorites from the database object
    for favorite in remove_favorites:
        # Skip the to-be removed favorite if not a current favorite
        if favorite in user_favorites_list:
            user_favorites_list.remove(favorite)
            print(f"{favorite} removed from favorites")
        else:
            print(f"{favorite} not in favorites")
    # Store updated database object back to the database
    user_favorites_doc_ref.set({"favorites": user_favorites_list})
    return jsonify({"message": "Provided favorites removed successfully"}), 200


# For logged-in user, get current favorite places
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    # User authentication
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return jsonify({"error": "authentication failed"}), 401
    # Get database favorites connection
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    # Return the database connection
    return jsonify({"favorites": user_favorites_list}), 200


# Providing AI-based travel/experience suggestions for the route
@app.route('/api/suggestions', methods=['GET'])
def generate_suggestion():
    # Read target location from the request
    location = request.args.get("input")
    # Create request for GPT
    message = [{"role": "user",
                "content": f"What are some things to do in {location}? Your answer should not exceed 25 words, and should be json-formatted containing the location and the address each."}]
    # Use GPT to get recommendations
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=message
    )
    reply = chat.choices[0].message.content
    # Return recommendations
    return jsonify({"places": reply})


# Use AI to make a unqiue/custom greetion
@app.route('/api/intro', methods=['GET'])
def generate_chatbot_hello():
    # Create the GPT request message
    message = [{"role": "user",
                "content": f"You are the assistant of a route planing system for transportation which considers co2 emissions. Say hello to the user, introduce yourself as the user's travel advisor. Your answer should not exceed 25 words."}]
    # Run the GPT query
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message
    )
    # Return the custom greeting to the frontend
    reply = chat.choices[0].message.content
    return jsonify({"intro": reply})


# Compute environment scores for given routes
def get_environment_score(from_loc, to_loc, gmaps_objects):
    # start = request.args.get("start")
    # end = request.args.get("end")
    # start = "Karlsruhe HBF"
    # end = "Istanbul"
    w_dist, w_dur, w_wp, w_r, b_dist, b_dur, b_wp, b_r, d_dist, d_dur, d_wp, d_r, p_dist, p_dur, p_wp, p_r = gmaps_objects

    # (w_dist, w_dur, w_wp, w_r) = GmapsUtils.calculate_route_gmaps(
    #     from_loc,
    #     to_loc,
    #     'walking'
    # )
    # print(f"{w_dist=}")
    # (b_dist, b_dur, b_wp, b_r) = GmapsUtils.calculate_route_gmaps(
    #     from_loc,
    #     to_loc,
    #     'biking'
    # )
    # print(f"{b_dist=}")

    # (d_dist, d_dur, d_wp, d_r) = GmapsUtils.calculate_route_gmaps(
    #     from_loc,
    #     to_loc,
    #     'driving'
    # )
    # print(f"{d_dist=}")

    # (p_dist, p_dur, p_wp, p_r) = GmapsUtils.calculate_route_gmaps(
    #     from_loc,
    #     to_loc,
    #     'transit'
    # )
    # print(f"{p_dist=}")

    text = f"You have to travel from {from_loc} to {to_loc}. Please rate each method with a singular score of 0 (least likely) to 100 (most likely) which transportation you would like to take if you consider CO2 emissions and travel time. You are an environmentally friendly person, but if the travel time is long or unrealistic, you prefer faster options. The following travel methods are available: walking, bicycle, driving, public_transportation, plane Give the results only (one score per travel method) back in JSON format."

    if w_dist is not None:
        text += f"\nTake the following information into consideration:\n"
        text += f"(walking distance (m), walking duration (sec))={(w_dist, w_dur)}"
        text += f"(public transportation distance (m), public transportation duration (sec))={(p_dist, p_dur)}"
        text += f"(driving distance (m), driving duration (sec))={(d_dist, d_dur)}"
        text += f"(bicycle distance (m), bicycle duration (sec))={(b_dist, b_dur)}"

    message = [{"role": "system", "content": text}]

    print(f"{message=}")
    chat = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=message
    )
    reply = chat.choices[0].message.content

    print(f"{reply=}")
    message.append({"role": "assistant", "content": reply})

    text_2 = f"Now provide a catastrophe score for how bad the climate change effects would be if the entire humanity took comparable routes every day. Give a score between 0 and 100 for each method. Give the results only (one score per travel method) in JSON format"

    text_2 += f"For the method 'car', also take into consideration the amount of maneuvers (left and right turns) it would take to realize the route whilst calculating the score. Amount of manuevers for method car: {len(GmapsUtils.get_maneuvers(d_r))}"

    message.append({"role": "system", "content": text_2})

    chat_2 = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",

        messages=message
    )
    reply_2 = chat_2.choices[0].message.content

    response_object = {}
    response_object['reply_1'] = reply
    response_object['reply_2'] = reply_2
    return response_object


def get_response(message):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=1,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0]["message"]["content"]


@app.route('/api/places', methods=['GET'])
def places_autocomplete():
    input = request.args.get("input")
    input = urllib.parse.quote(input)
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input}&key={GMAPS_KEY}"
    places_response = requests.get(url).json()
    predictions = []
    for prediction_obj in places_response['predictions']:
        predictions.append(prediction_obj['description'])
    return jsonify(predictions)


@app.route('/api/routes', methods=['GET'])
def routing():
    from_loc = request.args.get("from")  # get data from frontend
    to_loc = request.args.get("to")  # get data from frontend

    (w_dist, w_dur, w_wp, w_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'walking'
    )
    (b_dist, b_dur, b_wp, b_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'bicycling'
    )
    (d_dist, d_dur, d_wp, d_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'driving'
    )
    (p_dist, p_dur, p_wp, p_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'transit'
    )

    gmaps_objects = (
    w_dist, w_dur, w_wp, w_r, b_dist, b_dur, b_wp, b_r, d_dist, d_dur, d_wp, d_r, p_dist, p_dur, p_wp, p_r)
    score_responses = get_environment_score(from_loc, to_loc, gmaps_objects)

    efficiency_scores = json.loads(score_responses.get('reply_1'))
    catastrophy_scores = json.loads(score_responses.get('reply_2'))
    response_data = {
        'walking': {
            'distance': w_dist,
            'duration': w_dur,
            'efficiency': efficiency_scores['walking'],
            'catastrophy': catastrophy_scores['walking'],
            'co2' : calculate_emissions(w_dist, 'walking'),
            'directionsResult': {
                'available_travel_modes': ['WALKING'],
                'geocoded_waypoints': w_wp,
                'routes': w_r,
            }
        },
        'biking': {
            'distance': b_dist,
            'duration': b_dur,
            'efficiency': efficiency_scores['bicycle'],
            'catastrophy': catastrophy_scores['bicycle'],
            'co2' : calculate_emissions(b_dist, 'bicycle'),
            'directionsResult': {
                'available_travel_modes': ['BICYCLING'],
                'geocoded_waypoints': b_wp,
                'routes': b_r,
            }
        },
        'driving': {
            'distance': d_dist,
            'duration': d_dur,
            'efficiency': efficiency_scores['driving'],
            'catastrophy': catastrophy_scores['driving'],
            'co2' : calculate_emissions(d_dist, 'driving'),
            'directionsResult': {
                'available_travel_modes': ['DRIVING'],
                'geocoded_waypoints': d_wp,
                'routes': d_r,
            }
        },
        'public': {
            'distance': p_dist,
            'duration': p_dur,
            'efficiency': efficiency_scores['public_transportation'],
            'catastrophy': catastrophy_scores['public_transportation'],
            'co2' : calculate_emissions(p_dist, 'public_transportation'),
            'directionsResult': {
                'available_travel_modes': ['TRANSIT'],
                'geocoded_waypoints': p_wp,
                'routes': p_r,
            },

        },
    }
    return jsonify(response_data)


@app.route('/api/user/routes', methods=['GET'])
def get_user_routes():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    # uid = 'hihoho'
    if uid is None:
        return jsonify({"message": "authentication failed"}), 401
    user_favorites_doc_ref = db.collection("user").document(uid)
    user_routes_collection_stream = user_favorites_doc_ref.collection("routes").stream()
    user_routes_collection = []
    for user_route in user_routes_collection_stream:
        user_routes_collection.append(user_route.to_dict())
    return jsonify(user_routes_collection)


@app.route('/api/user/routes', methods=['POST'])
def add_user_route():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    # uid = 'hihoho'
    if uid is None:
        return jsonify({"message": "authentication failed"}), 401
    new_route = request.json
    new_route = {
        "from": new_route['from'],
        "to": new_route['to'],
        "duration": new_route['duration'],
        "distance": new_route['distance'],
        "efficiency": new_route['efficiency'],
        "catastrophy": new_route['catastrophy'],
        "datetime": new_route['datetime'],
        "mode": new_route['mode']
    }
    user_routes_collection_ref = db.collection("user").document(uid).collection("routes")
    user_routes_collection_ref.add(new_route)
    return jsonify({"message": "successfully added route to personal user routes"}), 200


@app.route('/api/user/score', methods=['GET'])
def get_user_score():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    # uid = 'KV91qiVsRDPakr9OxV456O2dgBE2'
    if uid is None:
        return jsonify({"message": "authentication failed"}), 401
    user_favorites_doc_ref = db.collection("user").document(uid)
    user_routes_collection_stream = user_favorites_doc_ref.collection("routes").stream()
    score = 0
    counter = 0
    for user_route in user_routes_collection_stream:
        user_rou = user_route.to_dict()
        score += user_rou['efficiency'] * user_rou['distance']
        counter += user_rou['distance']
    score /= counter
    return jsonify({"score": score})


# @app.route('/api/emissions', methods=['GET'])
def calculate_emissions(distance, mode):
    # distance = request.args.get("distance")
    # mode = request.args.get("mode")
    
    distance_in_km =  distance / 1000

    if mode == "walking" or mode in "biking":
        emissions = 0
    elif mode == "car":
        emissions = Mode.SMALL_CAR.estimate_co2(distance_in_km)
    elif mode == "public_transportation":
        emissions = Mode.LIGHT_RAIL.estimate_co2(distance_in_km)
    elif mode == "plane":
        emissions = Mode.AIRPLANE.estimate_co2(distance_in_km)
    else:
        print("Invalid mode of transportation.")
        return None

    # return jsonify({"emissions": emissions})
    return emissions


# # this method calculates an efficiency score based on time and co2 emissions
# def calculate_efficiency(distance, travel_mode, min_travel_time, max_travel_time, travel_time):
#     min_co2_emissions = min(Mode.SMALL_CAR.estimate_co2(distance_in_km=distance) / 25,
#                             Mode.SMALL_CAR.estimate_co2(distance_in_km=distance),
#                             Mode.LIGHT_RAIL.estimate_co2(distance_in_km=distance),
#                             Mode.AIRPLANE.estimate_co2(distance_in_km=distance))
#     max_co2_emissions = max(Mode.SMALL_CAR.estimate_co2(distance_in_km=distance) / 25,
#                             Mode.SMALL_CAR.estimate_co2(distance_in_km=distance),
#                             Mode.LIGHT_RAIL.estimate_co2(distance_in_km=distance),
#                             Mode.AIRPLANE.estimate_co2(distance_in_km=distance))

#     # we have to invert the travel time -> the shorter the better
#     normalized_travel_time = 1 - (travel_time - min_travel_time) / (max_travel_time - min_travel_time)

#     # we have to invert the emissions -> the lower the better
#     co2_emissions = calculate_emissions(distance, travel_mode)
#     normalized_co2_emissions = 1 - (co2_emissions - min_co2_emissions) / (max_co2_emissions - min_co2_emissions)

#     # here we set the weights, which is more important to us. in total they should sum up to
#     travel_time_weight = 0.6
#     co2_emissions_weight = 0.4

#     efficiency_score = (
#                                    normalized_travel_time * travel_time_weight + normalized_co2_emissions * co2_emissions_weight) * 100
#     return efficiency_score


if __name__ == '__main__':
    app.run()
