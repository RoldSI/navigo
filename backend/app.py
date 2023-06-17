from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, auth

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

@app.route('/api/favorites/add', methods=['POST'])
def add_favorite():
    data = request.get_json()
    if 'favorite' in data:
        favorite = data['favorite']
        favorites.append(favorite)
        return jsonify({'message': 'Favorite added successfully'})
    else:
        return jsonify({'message': 'Invalid request'})

@app.route('/api/favorites/remove', methods=['POST'])
def remove_favorite():
    data = request.get_json()
    if 'favorite' in data:
        favorite = data['favorite']
        if favorite in favorites:
            favorites.remove(favorite)
            return jsonify({'message': 'Favorite removed successfully'})
        else:
            return jsonify({'message': 'Favorite not found'})
    else:
        return jsonify({'message': 'Invalid request'})

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


if __name__ == '__main__':
    app.run()
