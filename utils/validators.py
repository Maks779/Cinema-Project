import re


class PasswordValidator:

    MIN_LENGTH = 8

    @staticmethod
    def validate(password):
        if not password:
            return False, "Password is required"

        if len(password) < PasswordValidator.MIN_LENGTH:
            return (
                False,
                f"Password must be at least {PasswordValidator.MIN_LENGTH} characters",
            )

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number"

        return True, ""


class UsernameValidator:

    MIN_LENGTH = 3
    MAX_LENGTH = 20

    @staticmethod
    def validate(username):
        if not username:
            return False, "Username is required"

        if len(username) < UsernameValidator.MIN_LENGTH:
            return (
                False,
                f"Username must be at least {UsernameValidator.MIN_LENGTH} characters",
            )

        if len(username) > UsernameValidator.MAX_LENGTH:
            return (
                False,
                f"Username must be no more than {UsernameValidator.MAX_LENGTH} characters",
            )

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers and underscores"

        return True, ""


class NameValidator:
    @staticmethod
    def validate(name, field_name="Name"):
        if not name:
            return False, f"{field_name} is required"

        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters"

        return True, ""
