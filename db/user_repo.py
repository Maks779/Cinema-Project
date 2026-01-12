from db.connection import get_db_connection


class UserRepo:
    def create_user(self, username, password, first_name, last_name):
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()
            # Simple SQL insert
            query = """
                INSERT INTO users (username, password_hash, first_name, last_name, role)
                VALUES (%s, %s, %s, %s, 'user')
            """
            cur.execute(query, (username, password, first_name, last_name))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            conn.close()

    def get_user_by_username(self, username):
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cur = conn.cursor()
            # Find user by username
            query = "SELECT id, username, password_hash, role, first_name, last_name FROM users WHERE username = %s"
            cur.execute(query, (username,))
            user = cur.fetchone()
            return user  # Returns a tuple or None if not found
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            conn.close()