from firebase_admin import auth
from flask import Flask, jsonify, request
import firebase_admin
from flask_cors import CORS
from firebase_admin import credentials, auth, firestore
import openai
from utils import GmapsUtils
from transport_co2 import Mode #https://pypi.org/project/transport-co2/
from dotenv import dotenv_values

env_vars = dotenv_values("../.env")
OPENAI_API_KEY = env_vars["OPENAI_API_KEY"]
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
        return 'authentication failed'
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
    return 'Provided favorites removed successfully'


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
    location = request.args.get("input") # get data from frontend
    message = [{"role": "user",
                "content": "What are some things to do in {location}? Your answer should not exceed 25 words, and should be json-formatted containing the location and the address each."}]
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=message
    )
    reply = chat.choices[0].message.content
    print("Reply: ", reply)
    return jsonify({"places": reply})


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
        'biking'
    )
    (d_dist, d_dur, d_wp, d_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'driving'
    )
    (p_dist, p_dur, p_wp, p_r) = GmapsUtils.calculate_route_gmaps(
        from_loc,
        to_loc,
        'public'
    )
    response_data = {
        'walking': {
            'distance': w_dist,
            'duration': w_dur,
            'efficiency': 100,
            'directionsResult': {
                'available_travel_modes': ['WALKING'],
                'geocoded_waypoints': w_wp,
                'routes': w_r,
            }
        },
        'biking': {
            'distance': b_dist,
            'duration': b_dur,
            'efficiency': 100,
            'directionsResult': {
                'available_travel_modes': ['BICYCLING'],
                'geocoded_waypoints': b_wp,
                'routes': b_r,
            }
        },
        'driving': {
            'distance': d_dist,
            'duration': d_dur,
            'efficiency': 100,
            'directionsResult': {
                'available_travel_modes': ['DRIVING'],
                'geocoded_waypoints': d_wp,
                'routes': d_r,
            }
        },
        'public': {
            'distance': p_dist,
            'duration': p_dur,
            'efficiency': 100,
            'directionsResult': {
                'available_travel_modes': ['TRANSIT'],
                'geocoded_waypoints': p_wp,
                'routes': p_r,
            }
        },
#         'plane': {
#             'distance': 30,  # meters
#             'time': 30,  # minutes
#             'efficiency': 34
#         }
    }

    return jsonify(response_data)


@app.route('/api/authenticateDemo', methods=['GET'])
def authentication_demo():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return 'authentication failed'
    else:
        return 'authentication successful'

def calculate_emissions(distance, mode):
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

    return emissions


if __name__ == '__main__':
    app.run()
