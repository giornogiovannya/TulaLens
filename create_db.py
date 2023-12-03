import sqlite3
import os

# Создание соединения с базой данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы users
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    login TEXT NOT NULL UNIQUE
                )''')

# Создание таблицы generations
cursor.execute('''CREATE TABLE IF NOT EXISTS generations (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    generation_number INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
