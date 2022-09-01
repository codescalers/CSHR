"""this file contains all validations inputs including mail, password etc.."""
import re


class Validator:
    """use this class to validate email ,password and name"""

    @staticmethod
    def validate_string(string: str) -> bool:
        """validate string method that vaidates a string is valid"""
        regex = re.compile('[@!#$%^&*()<>?/\b}{-~:"]')
        return True if (regex.search(string) is None) else False

    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password method that confirms if this valid password or not"""
        if re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", password):
            return True
        return False

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email method that confirms if this valid email or not"""
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return email if (re.fullmatch(regex, email)) else None
