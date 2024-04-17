#!/usr/bin/env python3

""" Session Authentication Module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Performs Session Authentication on the API"""

    user_id_by_session_id = {}

    def __init__(self) -> None:
        """Initializes the class"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        Return:
            - None if user_id is None
            - None if user_id is not a string
            - session_id otherwise
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Fetches a User ID based on a Session ID
        Return:
            - None if session_id is None
            - None if session_id is not a string
            - the User ID for the key session_id in the dictionary
                user_id_by_session_id otherwise
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
