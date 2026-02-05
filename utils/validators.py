import re


class PasswordValidator:
    """Валідація пароля"""
    
    MIN_LENGTH = 8
    
    @staticmethod
    def validate(password):
        """
        Перевіряє пароль на відповідність вимогам
        
        Вимоги:
        - Мінімум 8 символів
        - Принаймні одна велика літера (A-Z)
        - Принаймні одна маленька літера (a-z)
        - Принаймні одна цифра (0-9)
        
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Password must be at least {PasswordValidator.MIN_LENGTH} characters"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        return True, ""


class UsernameValidator:
    """Валідація username"""
    
    MIN_LENGTH = 3
    MAX_LENGTH = 20
    
    @staticmethod
    def validate(username):
        """
        Перевіряє username
        
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not username:
            return False, "Username is required"
        
        if len(username) < UsernameValidator.MIN_LENGTH:
            return False, f"Username must be at least {UsernameValidator.MIN_LENGTH} characters"
        
        if len(username) > UsernameValidator.MAX_LENGTH:
            return False, f"Username must be no more than {UsernameValidator.MAX_LENGTH} characters"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers and underscores"
        
        return True, ""


class NameValidator:
    """Валідація імені"""
    
    @staticmethod
    def validate(name, field_name="Name"):
        """
        Перевіряє ім'я
        
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not name:
            return False, f"{field_name} is required"
        
        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters"
        
        return True, ""
