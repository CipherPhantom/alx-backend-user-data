#!/usr/bin/env python3

""" Basic Authentication Module
"""
from api.v1.auth.auth import Auth
import base64


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
            decoded = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return decoded.decode('utf-8')

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
        return tuple(decoded_base64_authorization_header.split(":"))
