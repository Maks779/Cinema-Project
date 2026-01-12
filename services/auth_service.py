from db.user_repo import UserRepo


class AuthService:
    def __init__(self):
        self.user_repo = UserRepo()
        self.current_user = None  # Stores logged-in user info

    def login(self, username, password) -> bool:
        # 1. Get user from DB
        user = self.user_repo.get_user_by_username(username)

        if user:
            # Database returns tuple: (id, username, password_hash, role, ...)
            db_password = user[2]

            # 2. Check if password matches
            # (Note: In Phase 7 we will add hashing, for now we check plain text)
            if db_password == password:
                self.current_user = user
                print(f"Login successful for: {username}")
                return True

        print("Login failed")
        return False

    def register(self, name, surname, username, password) -> bool:
        # Check if user already exists
        if self.user_repo.get_user_by_username(username):
            print("Username already taken")
            return False

        # Create new user
        return self.user_repo.create_user(username, password, name, surname)