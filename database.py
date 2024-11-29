    import sqlite3

    class DatabaseError(Exception):
        """Класс исключений для ошибок базы данных"""
        pass
    class Database:

        def __init__(self, db_name='time_tracking.db'):
            self.connection = sqlite3.connect(db_name)
            self.connection.execute('PRAGMA foreign_keys = ON')

        def create_tables(self):
            with self.connection:
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        rank TEXT
                    )
                ''')
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS work_hours (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        hours INTEGER,
                        break_time INTEGER,
                        sick_leave TEXT,
                        vacation TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )
                ''')

        def register_user(self, username, password):
            try:
                with self.connection:
                    self.connection.execute('INSERT INTO users (username, password, rank) VALUES (?, ?, ?)',
                                            (username, password, 'сотрудник'))
                return True
            except sqlite3.IntegrityError:
                print("Ошибка: Имя пользователя уже используется.")
                return False
            except Exception as e:
                print(f"Ошибка базы данных: {e}")
                return False

        def login_user(self, username, password):
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            return cursor.fetchone()

        def submit_hours(self, user_id, hours, break_time, sick_leave, vacation):
            with self.connection:
                self.connection.execute(
                    'INSERT INTO work_hours (user_id, hours, break_time, sick_leave, vacation) VALUES (?, ?, ?, ?, ?)',
                    (user_id, hours, break_time, sick_leave, vacation))

        def get_work_hours(self):
            cursor = self.connection.cursor()
            cursor.execute(
                'SELECT username, SUM(hours) FROM work_hours JOIN users ON work_hours.user_id = users.id GROUP BY username')
            return cursor.fetchall()

        def close(self):
            self.connection.close()
