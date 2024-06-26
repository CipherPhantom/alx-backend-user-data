#!/usr/bin/env python3

""" Basic Authentication Module
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Performs Basic Authentication on the API"""

    def __init__(self) -> None:
        """Initializes the class"""
        super().__init__()

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
            header for a Basic Authentication
        Return:
            - None if authorization_header is None
            - None if authorization_header is not a string
            - None if authorization_header doesn’t start by Basic
                (with a space at the end)
            - The value after Basic (after the space) otherwise
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decodes value of a Base64 string
        Returns:
            - None if base64_authorization_header is None
            - None if base64_authorization_header is not a string
            - None if base64_authorization_header is not a valid Base64
            - The decoded value as UTF8 string otherwise
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None
        return decoded

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user credentials from the Base64 decoded value
        Returns:
            -  2 values
            - None, None if decoded_base64_authorization_header is None
            - None, None if decoded_base64_authorization_header is not a string
            - None, None if decoded_base64_authorization_header doesn’t contain
            - the user email and the user password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        decoded_list = decoded_base64_authorization_header.split(":")
        return decoded_list[0], ":".join(decoded_list[1:])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Creates the User instance based on his email and password.
        Returns:
            - None if user_email is None or not a string
            - None if user_pwd is None or not a string
            - None if your database (file) doesn’t contain any User
            instance with email equal to user_email
            - None if user_pwd is not the password of the User instance found
            - The User instance otherwise
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if len(users) == 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        auth_header_b64 = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(auth_header_b64)
        user_credentials = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
            user_email=user_credentials[0],
            user_pwd=user_credentials[1]
            )
        return user
