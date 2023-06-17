from firebase_admin import auth
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, auth
import openai
from utils import GmapsUtils
from dotenv import dotenv_values

env_vars = dotenv_values("../.env")
OPENAI_API_KEY = env_vars["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY
cred = credentials.Certificate('firebaseCredentials.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)
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
    favorite = request.json['input']
    favorites.append(favorite)
    response = {'message': 'Favorite added successfully'}
    return jsonify(response)


@app.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    favorite = request.json['input']
    if favorite in favorites:
        favorites.remove(favorite)
        response = {'message': 'Favorite removed successfully'}
    else:
        response = {'message': 'Favorite not found'}
    return jsonify(response)


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    return 'this should return favorites'


@app.route('/api/suggestions', methods=['GET'])
def generate_suggestion():
  location = request.json['input'] #get data from frontend
  message = [ {"role": "user", "content": f"What are some things to do in {location}? Your answer should not exceed 25 words."} ]
  chat = openai.ChatCompletion.create(
      model="gpt-4", messages=message
  )
  reply = chat.choices[0].message.content
  return reply


@app.route('/api/routes', methods=['GET'])
def routing():
    #request_data = request.args
    #from_param = request_data.get('from')
    #to_param = request_data.get('to')
    request_data = {
        'from': 'Berlin',
        'to': 'Munich',
    }
    (decoded_points, gm, distance, duration) = GmapsUtils.calculate_route_gmaps(request_data['from'], request_data['to'], 'walking')
    response_data = {
        'walking': {
            'distance': distance,  # meters
            'duration': duration,  # minutes
            'decoded_points': decoded_points,  # array of waypoints
            'efficiency': 34  # (1)/((time * factor) * (co2 * factor))
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


if __name__ == '__main__':
    app.run()
