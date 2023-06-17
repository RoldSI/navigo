from flask import Flask, jsonify, request

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
    bearer_token = request.headers.get('Authorization')
    uid = authenticate_user(bearer_token)
    if uid is None:
        return 'authentication failed'
    else:
        return 'authentication successful'


if __name__ == '__main__':
    app.run()
