from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    response = {
        'ping': 'pong',
        'aboba': 'boba'
    }
    return jsonify(response)


@app.route('/send_pdf', methods=['POST'])
def upload_pdf():
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
    photo_index = 0
    photos = []
    while f'photo{photo_index}' in request.files:
        photos.extend(request.files.getlist(f'photo{photo_index}'))
        photo_index += 1

    if not photos:
        return jsonify({'error': 'No photos part'})

    for idx, photo in enumerate(photos):
        photo.save(f'/home/aboba/TulaLens/static/photo_{idx}.jpg')

    return jsonify({'message': 'Photos uploaded successfully'})


@app.route('/get_pdf')
def get_pdf():
    print('Послал пдфку')
    return send_file('home/aboba/TulaLens/sample.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
