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
    print(location)
    message = [{"role": "user",
                "content": f"What are some things to do in {location}?
                Your answer should not exceed 25 words, and should be json-formatted containing the
                location and the address each."}]
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=message
    )
    reply = chat.choices[0].message.content
    print("Reply: ", reply)
    return jsonify({"places": reply})


@app.route('/api/routes', methods=['GET'])
def routing():
    # request_data = request.args
    # from_param = request_data.get('from')
    # to_param = request_data.get('to')
    request_data = {
        'from': 'Berlin',
        'to': 'Munich',
    }
    (w_dp, w_gm, w_di, w_du) = GmapsUtils.calculate_route_gmaps(
        request_data['from'],
        request_data['to'],
        'walking'
    )
    (b_dp, b_gm, b_di, b_du) = GmapsUtils.calculate_route_gmaps(
        request_data['from'],
        request_data['to'],
        'biking'
    )
    (d_dp, d_gm, d_di, d_du) = GmapsUtils.calculate_route_gmaps(
        request_data['from'],
        request_data['to'],
        'driving'
    )
    (p_dp, p_gm, p_di, p_du) = GmapsUtils.calculate_route_gmaps(
        request_data['from'],
        request_data['to'],
        'public'
    )
    response_data = {
        'walking': {
            'distance': w_di,  # meters
            'duration': w_du,  # minutes
            'decoded_points': w_dp,  # array of waypoints
            'efficiency': 100  # (1)/((time * factor) * (co2 * factor))
        },
        'biking': {
            'distance': 30,  # meters
            'time': 30,  # minutes
            'efficiency': 34
        },
        'driving': {
            'distance': 30,  # meters
            'time': 30,  # minutes
            'efficiency': 34
        },
        'public': {
            'distance': 30,  # meters
            'time': 30,  # minutes
            'efficiency': 34
        },
        'plane': {
            'distance': 30,  # meters
            'time': 30,  # minutes
            'efficiency': 34
        }
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
