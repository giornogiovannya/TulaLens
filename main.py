from flask import Flask, request, jsonify

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
        file.save('/home/aboba/TulaLens/' + file.filename)
        return jsonify({'message': 'File uploaded successfully'})


@app.route('/upload_photos', methods=['POST'])
def upload_photos():
    if 'photo0' not in request.files:
        return jsonify({'error': 'No photos part'})

    photos = request.files.getlist('photo0')

    for idx, photo in enumerate(photos):
        photo.save(f'/home/aboba/static/photo_{idx}.jpg')

    return jsonify({'message': 'Photos uploaded successfully'})


if __name__ == '__main__':
    app.run(debug=True)
