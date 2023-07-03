import sqlite3

class Database:
    def __init__(self, db_name):
        # Создание подключения к базе данных SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Создание таблицы, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_date TEXT
            )
        ''')
        self.conn.commit()

    def insert_user(self, user_id, username, first_name, last_name):
        # Вставка данных в базу данных
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, created_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()

    def close_connection(self):
        # Закрытие подключения к базе данных
        self.cursor.close()
        self.conn.close()
