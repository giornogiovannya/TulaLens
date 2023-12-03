from flask import Flask, request, jsonify, send_file
import sqlite3
import shutil


app = Flask(__name__)


def check_user_exists(login):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    user = cursor.fetchone()
    conn.close()
    return user


# Маршрут для авторизации и регистрации
@app.route('/authenticate', methods=['POST'])
def authenticate():
    login = request.json.get('login')

    # Проверка существования пользователя
    user = check_user_exists(login)

    if user:
        return jsonify({'status': 'error', 'message': 'Логин уже занят'}), 400
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Регистрация нового пользователя
        cursor.execute("INSERT INTO users (login) VALUES (?)", (login,))
        conn.commit()
        conn.close()

        return jsonify({'status': 'ok', 'message': 'Пользователь зарегистрирован'}), 200


# Функция для создания папки пользователя и генерации пути для сохранения файла
def create_user_folder(user_id, request_number):
    user_folder = f"user_{user_id}"
    request_folder = f"request_{request_number}"
    path = os.path.join(user_folder, request_folder)

    os.makedirs(path, exist_ok=True)
    return path


# Маршрут для приема документов
@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    login = request.form.get('login')
    agreement_files = request.files.getlist('agreement')
    claim_files = request.files.getlist('claim')
    calculate_files = request.files.getlist('calculate')

    # Получение ID пользователя из базы данных
    user_id = get_user_id(login)

    # Создание папки пользователя и номера запроса
    request_number = get_request_number()
    path = create_user_folder(user_id, request_number)

    for idx, file in enumerate(agreement_files):
        if file.filename.endswith('.jpg'):
            file.save(os.path.join(path, 'agreement', f'photo_{idx + 1}.jpg'))
        elif file.filename.endswith('.pdf'):
            file.save(os.path.join(path, 'agreement', 'file.pdf'))

    for idx, file in enumerate(claim_files):
        if file.filename.endswith('.jpg'):
            file.save(os.path.join(path, 'claim', f'photo_{idx + 1}.jpg'))
        elif file.filename.endswith('.pdf'):
            file.save(os.path.join(path, 'claim', 'file.pdf'))

    for idx, file in enumerate(calculate_files):
        if file.filename.endswith('.jpg'):
            file.save(os.path.join(path, 'calculate', f'photo_{idx + 1}.jpg'))
        elif file.filename.endswith('.pdf'):
            file.save(os.path.join(path, 'calculate', 'file.pdf'))


    return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)
    #return jsonify({'status': 'ok', 'message': 'Документы сохранены'}), 200


@app.route('/get_pdf')
def get_pdf():
    print('Послал пдфку')
    return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
