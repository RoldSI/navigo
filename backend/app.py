from firebase_admin import auth
from flask import Flask, jsonify, request
import firebase_admin
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
    # uid = 'hoi'
    if uid is None:
        return 'authentication failed'
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    print(user_favorites_list)
    new_favorites = request.json['input']
    for favorite in new_favorites:
        if favorite not in user_favorites_list:
            user_favorites_list.append(favorite)
            print(f"{favorite} added to favorites")
        else:
            print(f"{favorite} already in favorites")
    user_favorites_doc_ref.set({"favorites": user_favorites_list})
    return 'Provided favorites added successfully'


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
    print(user_favorites_list)
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
        return 'authentication failed'
    user_favorites_doc_ref = db.collection("favorites").document(uid)
    user_favorites_list = user_favorites_doc_ref.get().to_dict()
    if user_favorites_list is None:
        user_favorites_list = []
    else:
        user_favorites_list = user_favorites_list["favorites"]
    print(user_favorites_list)
    return jsonify({"favorites": user_favorites_list})


@app.route('/api/suggestions', methods=['GET'])
def generate_suggestion():
    location = request.json['input']  # get data from frontend
    message = [{"role": "user",
                "content": f"What are some things to do in {location}? Your answer should not exceed 25 words."}]
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=message
    )
    reply = chat.choices[0].message.content
    return reply


@app.route('/api/routes', methods=['GET'])
def routing():
    request_data = request.args
    from_param = request_data.get('from')
    to_param = request_data.get('to')
    (w_dp, w_gm, w_di, w_du) = GmapsUtils.calculate_route_gmaps(
        from_param,
        to_param,
        'walking'
    )
    (b_dp, b_gm, b_di, b_du) = GmapsUtils.calculate_route_gmaps(
        from_param,
        to_param,
        'bicycling'
    )
    (d_dp, d_gm, d_di, d_du) = GmapsUtils.calculate_route_gmaps(
        from_param,
        to_param,
        'driving'
    )
    (t_dp, t_gm, t_di, t_du) = GmapsUtils.calculate_route_gmaps(
        from_param,
        to_param,
        'transit'
    )
    response_data = {
        'walking': {
            'response': w_gm,
            'distance': w_di,  # meters
            'duration': w_du,  # minutes
            'decoded_points': w_dp,  # array of waypoints
            'efficiency': 100  # (1)/((time * factor) * (co2 * factor))
        },
        'bicycling': {
            'response': b_gm,
            'distance': b_di,  # meters
            'duration': b_du,  # minutes
            'decoded_points': b_dp,  # array of waypoints
            'efficiency': 100  # (1)/((time * factor) * (co2 * factor))
        },
        'driving': {
            'response': d_gm,
            'distance': d_di,  # meters
            'duration': d_du,  # minutes
            'decoded_points': d_dp,  # array of waypoints
            'efficiency': 100  # (1)/((time * factor) * (co2 * factor))
        },
        'transit': {
            'response': t_gm,
            'distance': t_di,  # meters
            'duration': t_du,  # minutes
            'decoded_points': t_dp,  # array of waypoints
            'efficiency': 100  # (1)/((time * factor) * (co2 * factor))
        }
    }
    return jsonify(response_data)


@app.route('/api/user/routes', methods=['GET'])
def get_user_routes():
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    uid = 'hihoho'
    if uid is None:
        return 'authentication failed'
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
    uid = 'hihoho'
    if uid is None:
        return 'authentication failed'
    new_route = request.json
    user_routes_collection_ref = db.collection("user").document(uid).collection("routes")
    user_routes_collection_ref.add(new_route)
    return 'successfully added route to personal user routes'


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
