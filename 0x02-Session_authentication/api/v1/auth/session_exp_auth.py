#!/usr/bin/env python3

""" Session Authentication Module with expiration
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Performs Session Authentication on the API with expiration"""

    def __init__(self) -> None:
        """Initializes the class"""
        super().__init__()
        try:
            duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Fetches a User ID based on a Session ID"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        user_id = session_dict.get("user_id")
        if self.session_duration <= 0:
            return user_id
        if "created_at" not in session_dict:
            return None
        created_at = session_dict.get("created_at")
        if timedelta(seconds=self.session_duration) + created_at < \
                datetime.now():
            return None
        return user_id
