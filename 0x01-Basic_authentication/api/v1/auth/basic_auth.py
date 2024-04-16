#!/usr/bin/env python3

""" Basic Authentication Module
"""
from api.v1.auth.auth import Auth


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
