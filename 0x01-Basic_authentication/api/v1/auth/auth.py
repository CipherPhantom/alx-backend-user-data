#!/usr/bin/env python3
"""
Authentication Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks which routes need authentication
        Returns:
            - True if path is None
            - True if excluded_paths is None or an empty list
            - False if path is in excluded_paths
            - True otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.endswith("*") and path.startswith(ex_path[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Validate all requests to secure the API
        Returns:
            - None If request is None
            - None If request doesn’t contain the header key Authorization
            - The value of the header request Authorization otherwise
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
