#!/usr/bin/env python3
""" Session Authentication Database Module
"""
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


UserSession.load_from_file()


class SessionDBAuth(SessionExpAuth):
    """Performs Session Authentication on the API with expiration
    for a database.
    """
    def create_session(self, user_id=None):
        """Creates and stores a new instance of UserSession
        Return:
            - Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {"user_id": user_id, "session_id": session_id}
        UserSession(**kwargs).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in
        the database based on session_id"""
        if session_id is None:
            return None
        try:
            user_sessions = UserSession.search({"session_id": session_id})
            if len(user_sessions) == 0:
                return None
        except Exception:
            return None
        user_id = user_sessions[0].user_id
        created_at = user_sessions[0].created_at
        if self.session_duration <= 0:
            return user_id
        if timedelta(seconds=self.session_duration) + created_at < \
                datetime.utcnow():
            return None
        return user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID
        from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        attributes = {"session_id": session_id, "user_id": user_id}
        try:
            user_sessions = UserSession.search(attributes)
            if len(user_sessions) == 0:
                return False
        except Exception:
            return False
        for user_session in user_sessions:
            user_session.remove()
        return True
