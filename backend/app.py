from flask import Flask, jsonify

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
