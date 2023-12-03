from flask import Flask, request, jsonify, send_file
import sqlite3
import shutil
import os


app = Flask(__name__)

USER_DATA_SAVE_PATH = "/home/aboba/TulaLens/TulaLens/user_data"


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

    conn.commit()
    conn.close()
    return jsonify({'status': 'ok', 'message': 'бд очищена'}), 200


def save_files(files, path, folder_name):
    for idx, file in enumerate(files):
        if file.filename.endswith('.jpg'):
            file.save(os.path.join(path, folder_name, f'photo_{idx + 1}.jpg'))
        elif file.filename.endswith('.pdf'):
            file.save(os.path.join(path, folder_name, 'file.pdf'))


@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    login = request.form.get('login')
    if login is None:
        # Вывод сообщения об ошибке или логирование
        return jsonify({'status': 'error', 'message': 'Отсутствует значение login'}), 400

    user_folder = os.path.join('user_data', login)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    agreement_files = request.files.getlist('agreement')
    claim_files = request.files.getlist('claim')
    calculate_files = request.files.getlist('calculate')
    print(agreement_files)

    text = agreement_files

    with open('output22322.txt', 'w') as file:
        file.write(text)

    print("CALC" + calculate_files)

    text = calculate_files

    with open('output2232343432.txt', 'w') as file:
        file.write(text)

    save_files(agreement_files, user_folder, 'agreement')
    save_files(claim_files, user_folder, 'claim')
    save_files(calculate_files, user_folder, 'calculate')

    # После выполнения операций все файлы удаляются
    #shutil.rmtree(user_folder)
    #return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)
    return jsonify({'status': 'ok', 'message': 'Документы обработаны и удалены'}), 200


@app.route('/get_pdf')
def get_pdf():
    print('Послал пдфку')
    return send_file('/home/aboba/TulaLens/sample.pdf', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
