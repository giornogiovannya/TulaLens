from flask import Flask

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    response = {
        'ping': 'pong',
        'aboba': 'boba'
    }
    return jsonify(response)


@app.route('/send_photo', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file.save('/path/to/save/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'})


if __name__ == '__main__':
    app.run(debug=True)
