import sqlite3

class Database:
    def __init__(self, db_name):
        # Create a connection to the SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the 'users' table if it doesn't exist
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

        # Create the 'user_question' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question TEXT,
                answer TEXT
            )
        ''')
        self.conn.commit()

        # Create the 'character' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "character" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                character TEXT
            )
        ''')
        self.conn.commit()

    def insert_user(self, user_id, username, first_name, last_name):
        # Insert data into the 'users' table
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, created_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()

    def insert_user_question_answer(self, user_id, question, answer):
        # Insert data into the 'user_question' table
        self.cursor.execute('''
            INSERT INTO user_question (user_id, question, answer)
            VALUES (?, ?, ?)
        ''', (user_id, question, answer))
        self.conn.commit()

    def insert_character(self, user_id, character):
        # Insert data into the 'character' table
        self.cursor.execute('''
            INSERT INTO "character" (user_id, character)
            VALUES (?, ?)
        ''', (user_id, character))
        self.conn.commit()

    def close_connection(self):
        # Close the database connection
        self.cursor.close()
        self.conn.close()
