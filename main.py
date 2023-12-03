from flask import Flask, request, jsonify, send_file
import sqlite3
import shutil
import os


app = Flask(__name__)

USER_DATA_SAVE_PATH = "/home/aboba/TulaLens/TulaLens/user_data"

def get_user_id(login):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE login=?", (login,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None


def get_request_number():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(generation_number) FROM generations")
    max_request_number = cursor.fetchone()[0]
    conn.close()
    return max_request_number + 1 if max_request_number else 1


def check_user_exists(login):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login=?", (login,))
    user = cursor.fetchone()
    conn.close()
    return user


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


@app.route('/clear_db_1234990', methods=['GET'])
def clear_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM generations")

    conn.commit()
    conn.close()
    return jsonify({'status': 'ok', 'message': 'Бд очищена'}), 200


# Функция для создания папки пользователя и генерации пути для сохранения файла
def create_user_folder(user_id, request_number):
    user_folder = f"user_{user_id}"
    request_folder = f"request_{request_number}"
    path = os.path.join(user_folder, request_folder)

    os.makedirs(path, exist_ok=True)
    return path


def save_files(files, path, folder_name):
    for idx, file in enumerate(files):
        if file.filename.endswith('.jpg'):
            file.save(os.path.join(path, folder_name, f'photo_{idx + 1}.jpg'))
        elif file.filename.endswith('.pdf'):
            file.save(os.path.join(path, folder_name, 'file.pdf'))


# Маршрут для приема документов
@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    login = request.form.get('login')
    agreement_files = request.files.getlist('agreement')
    claim_files = request.files.getlist('claim')
    calculate_files = request.files.getlist('calculate')

    # Создание папки с данными
    user_id = get_user_id(login)
    request_number = get_request_number()
    path = create_user_folder(user_id, request_number)



    save_files(agreement_files, path, 'agreement')
    save_files(claim_files, path, 'claim')
    save_files(calculate_files, path, 'calculate')


    return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)
    #return jsonify({'status': 'ok', 'message': 'Документы сохранены'}), 200


@app.route('/get_pdf')
def get_pdf():
    print('Послал пдфку')
    return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
