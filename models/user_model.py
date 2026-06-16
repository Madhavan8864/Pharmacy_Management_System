from database.db import get_db_connection

class UserModel:
    @staticmethod
    def create_user(username, password, role='staff'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      (username, password, role))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    @staticmethod
    def get_user_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user