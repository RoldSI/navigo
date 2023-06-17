from flask import Flask, jsonify, request
import firebase_admin
from flask_cors import CORS
from firebase_admin import credentials, auth, firestore
import openai
from utils import GmapsUtils
from transport_co2 import Mode #https://pypi.org/project/transport-co2/
from dotenv import dotenv_values
import urllib
import requests
import json


env_vars = dotenv_values(".env")
OPENAI_API_KEY = env_vars["OPENAI_API_KEY"]
GMAPS_KEY = env_vars["GMAPS_KEY"]
openai.api_key = OPENAI_API_KEY

cred = credentials.Certificate('firebaseCredentials.json')
firebaseApp = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

CORS(app)  # Enable CORS for all routes
favorites = []


def authenticate_user(bearer_token):
    if bearer_token is None:
        return None
    try:
        decoded_token = auth.verify_id_token(bearer_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        # Authentication failed
        return None


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return jsonify({"error": "authentication failed"}), 401
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]

    new_favorites = request.json['input']
    print("FAV: ", new_favorites)


    for favorite in new_favorites:
        if favorite not in user_favorites_list:
            user_favorites_list.append(favorite)
            print(f"{favorite} added to favorites")
        else:
            print(f"{favorite} already in favorites")

    user_favorites_doc_ref.set({"favorites": user_favorites_list})
    return jsonify({"message": "Provided favorites added successfully"}), 200


@app.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    # uid = 'hoi'
    if uid is None:
        return jsonify({"message": "authentication failed"}), 401
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    remove_favorites = request.json['input']
    for favorite in remove_favorites:
        if favorite in user_favorites_list:
            user_favorites_list.remove(favorite)
            print(f"{favorite} removed from favorites")
        else:
            print(f"{favorite} not in favorites")
    user_favorites_doc_ref.set({"favorites": user_favorites_list})
    return jsonify({"message": "Provided favorites removed successfully"}), 200


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    # uid = 'hoi'
    if uid is None:
        return jsonify({"error": "authentication failed"}), 401
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    return jsonify({"favorites": user_favorites_list}), 200


@app.route('/api/suggestions', methods=['GET'])
def generate_suggestion():
    location = request.args.get("input")
    #location = request.json['input']  # get data from frontend
    message = [{"role": "user",
                "content": f"What are some things to do in {location}? Your answer should not exceed 25 words, and should be json-formatted containing the location and the address each."}]
    # actual version
    '''chat = openai.ChatCompletion.create(
        model="gpt-4", messages=message
    )
    reply = chat.choices[0].message.content
    print(reply)
    return jsonify({"places": reply})'''
    # dummy because we're poor
    return jsonify(
        {
            "places": "{\n  \"1\": {\"location\": \"ZKM | Center for Art and Media\", \"address\": \"Lorenzstr. 19, 76135 Karlsruhe\"},\n  \"2\": {\"location\": \"Karlsruhe Palace\", \"address\": \"Schloßbezirk 10, 76131 Karlsruhe\"},\n  \"3\": {\"location\": \"Botanical Gardens\", \"address\": \"Ernst-Friedrich-Platz 5, 76133 Karlsruhe\"}\n}"
        }
    )


@app.route('/api/intro', methods=['GET'])
def generate_chatbot_hello():
    message = [{"role": "user",
                "content": f"You are the assistant of a route planing system for transportation which considers co2 emissions. Say hello to it, introduce yourself Your answer should not exceed 25 words."}]
    # actual stuff
    '''chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message
    )
    reply = chat.choices[0].message.content
    return jsonify({"intro": reply})'''
    # dummy because we're poor
    return jsonify({
        "intro": "Hello, I'm the AI assistant of a route planning system that considers CO2 emissions. How can I assist you today?"
    })


# @app.route('/api/efficiency_score', methods=['GET'])
def get_environment_score(from_loc, to_loc, gmaps_objects):
    # start = request.args.get("start")
    # end = request.args.get("end")
    # start = "Karlsruhe HBF"
    # end = "Istanbul"
    w_dist, w_dur, w_wp, w_r, b_dist, b_dur, b_wp, b_r, d_dist, d_dur, d_wp, d_r, p_dist, p_dur, p_wp, p_r = gmaps_objects

    (w_dist, w_dur, w_wp, w_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'walking'
    )
    print(f"{w_dist=}")
    (b_dist, b_dur, b_wp, b_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'biking'
    )
    print(f"{b_dist=}")

    (d_dist, d_dur, d_wp, d_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'driving'
    )
    print(f"{d_dist=}")

    (p_dist, p_dur, p_wp, p_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'transit'
    )
    print(f"{p_dist=}")



    text = f"You have to travel from {from_loc} to {to_loc}. Please rate each method with a singular score of 0 (least likely) to 100 (most likely) which transportation you would like to take if you consider CO2 emissions and travel time. You are an environmentally friendly person, but if the travel time is long or unrealistic, you prefer faster options. The following travel methods are available: walking, bicycle, driving, public_transportation, plane Give the results only (one score per travel method) back in JSON format."
    
    if w_dist is not None:
        text += f"\nTake the following information into consideration:\n"
        text += f"(walking distance (m), walking duration (min))={(w_dist, w_dur)}"
        text += f"(public transportation distance (m), public transportation duration (min))={(p_dist, p_dur)}"
        text += f"(driving distance (m), driving duration (min))={(d_dist, d_dur)}"
        text += f"(bicycle distance (m), bicycle duration (min))={(b_dist, b_dur)}"



    message = [{"role": "system", "content": text}]

    print(f"{message=}")
    chat = openai.ChatCompletion.create(
        # model="gpt-4",
        model="gpt-3.5-turbo",
        messages=message
    )
    reply = chat.choices[0].message.content

    print(f"{reply=}")
    message.append({"role":"assistant", "content": reply})

    

    text_2 = f"Now provide a catastrophe score for how bad the climate change effects would be if the entire humanity took comparable routes every day. Give a score between 0 and 100 for each method. Give the results only (one score per travel method) in JSON format"

    text_2 += f"For the method 'car', also take into consideration the amount of maneuvers (left and right turns) it would take to realize the route whilst calculating the score. Amount of manuevers for method car: {len(GmapsUtils.get_maneuvers(d_r))}"
    

    message.append({"role":"system", "content": text_2})

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
        model = 'gpt-3.5-turbo',
        temperature = 1,
        messages = [
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0]["message"]["content"]





@app.route('/api/places', methods=['Get'])
def places_autocomplete():
    input = request.args.get("input")
    input = urllib.parse.quote(input)
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input}&key={GMAPS_KEY}"
    places_response = requests.get(url).json()
    predictions = []
    for prediction_obj in places_response['predictions']:
        predictions.append(prediction_obj['structured_formatting']['main_text'])
    return jsonify(predictions)


@app.route('/api/routes', methods=['GET'])
def routing():
    from_loc = request.args.get("from") # get data from frontend
    to_loc = request.args.get("to") # get data from frontend

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

    

    gmaps_objects = (w_dist, w_dur, w_wp, w_r, b_dist, b_dur, b_wp, b_r, d_dist, d_dur, d_wp, d_r, p_dist, p_dur, p_wp, p_r)
    score_responses = get_environment_score(from_loc, to_loc, gmaps_objects)



    efficiency_scores = json.loads(score_responses.get('reply_1'))
    catastrophy_scores = json.loads(score_responses.get('reply_2'))
    response_data = {
        'walking': {
            'distance': w_dist,
            'duration': w_dur,
            'efficiency': efficiency_scores['walking'],
            'catastrophy': catastrophy_scores['walking'],
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
            'directionsResult': {
                'available_travel_modes': ['TRANSIT'],
                'geocoded_waypoints': p_wp,
                'routes': p_r,
            }
        },
        'plane': {
            'efficiency': efficiency_scores['plane'],
            'catastrophy': catastrophy_scores['plane'],
        }
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
    user_routes_collection_ref = db.collection("user").document(uid).collection("routes")
    user_routes_collection_ref.add(new_route)
    return jsonify({"message": "successfully added route to personal user routes"}), 200


@app.route('/api/emissions', methods=['GET'])
def calculate_emissions(distance, mode):
    distance = request.args.get("distance")
    mode = request.args.get("mode")
    if mode == "walking" or mode in "biking":
        if distance == 0:
          emissions = 0
        else:
          emissions = Mode.SMALL_CAR.estimate_co2(distance_in_km=distance)/25
    elif mode == "car":
        emissions = Mode.SMALL_CAR.estimate_co2(distance_in_km=distance)
    elif mode == "public_transportation":
        emissions = Mode.LIGHT_RAIL.estimate_co2(distance_in_km=distance)
    elif mode == "plane":
        emissions = Mode.AIRPLANE.estimate_co2(distance_in_km=distance)
    else:
        print("Invalid mode of transportation.")
        return None

    return jsonify({"emissions": emissions})


#this method calculates an efficiency score based on time and co2 emissions
def calculate_efficiency(distance, travel_mode, min_travel_time, max_travel_time, travel_time):
    min_co2_emissions = min(Mode.SMALL_CAR.estimate_co2(distance_in_km=distance)/25, Mode.SMALL_CAR.estimate_co2(distance_in_km=distance), 
                          Mode.LIGHT_RAIL.estimate_co2(distance_in_km=distance), Mode.AIRPLANE.estimate_co2(distance_in_km=distance))
    max_co2_emissions = max(Mode.SMALL_CAR.estimate_co2(distance_in_km=distance)/25, Mode.SMALL_CAR.estimate_co2(distance_in_km=distance), 
                          Mode.LIGHT_RAIL.estimate_co2(distance_in_km=distance), Mode.AIRPLANE.estimate_co2(distance_in_km=distance))
    
    #we have to invert the travel time -> the shorter the better
    normalized_travel_time = 1 - (travel_time - min_travel_time) / (max_travel_time - min_travel_time)
    
    #we have to invert the emissions -> the lower the better
    co2_emissions = calculate_emissions(distance, travel_mode)
    normalized_co2_emissions = 1 - (co2_emissions - min_co2_emissions) / (max_co2_emissions - min_co2_emissions)
    
    #here we set the weights, which is more important to us. in total they should sum up to 
    travel_time_weight = 0.6
    co2_emissions_weight = 0.4

    efficiency_score = (normalized_travel_time * travel_time_weight + normalized_co2_emissions * co2_emissions_weight) * 100
    return efficiency_score


if __name__ == '__main__':
    app.run()
