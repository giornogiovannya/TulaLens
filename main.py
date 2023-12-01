from flask import Flask

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    response = {
        'ping': 'pong',
        'aboba': 'boba'
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
