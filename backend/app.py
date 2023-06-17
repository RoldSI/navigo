from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, auth
import openai

openai.api_key = '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'
cred = credentials.Certificate('firebaseCredentials.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__)
favorites = []

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from the backend api data!'}
    return jsonify(data)


@app.route('/api/backend', methods=['GET'])
def get_index():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    favorite = request.json['input']
    favorites.append(favorite)
    response = {'message': 'Favorite added successfully'}
    return jsonify(response)

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    favorite = request.json['input']
    if favorite in favorites:
        favorites.remove(favorite)
        response = {'message': 'Favorite removed successfully'}
    else:
        response = {'message': 'Favorite not found'}
    return jsonify(response)

@app.route('/authenticate', methods=['GET'])
def authenticate_user():
    id_token = request.json['idToken']
    '''try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        # Authentication successful
        # You can now use the 'uid' to identify the user and perform further actions
        return 'Authentication successful'
    except auth.AuthError as e:
        # Authentication failed
        return str(e), 401'''
    return 'shit'
    #data = {'message': 'Hello from the backend!'}
    #return jsonify(data)

@app.route('/suggestions', methods=['POST'])
def generate_suggestion():
  location = request.json['input'] #get data from frontend
  message = [ {"role": "user", "content": f"What are some things to do in {location}? Your answer should not exceed 25 words."} ]

  chat = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", messages=message
    )
  reply = chat.choices[0].message.content
  return reply

if __name__ == '__main__':
    app.run()
