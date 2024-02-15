#!/usr/bin/env python3
"""
Defines SessionExpAuth class that implements session expiration
"""
import os
from datetime import datetime, timedelta
from typing import Union

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Session Authentication class with expiration
    """
    def __init__(self):
        """
        Instialize a SessionExpAuth instance
        """
        super().__init__()
        try:
            duration = int(os.environ.get('SESSION_DURATION', 0))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None) -> Union[str, None]:
        """
        Create session id from random string
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id, 'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None) -> Union[str, None]:
        """
        Get user id from given session id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        if timedelta(seconds=self.session_duration) + \
                session_dictionary.get('created_at') <= datetime.now():
            return None
        return session_dictionary.get('user_id')
