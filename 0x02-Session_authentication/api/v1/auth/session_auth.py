#!/usr/bin/env python3
"""
Session authentication module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict, TypeVar
from uuid import uuid4
from os import getenv


class SessionAuth(Auth):
    """ Session Authentication implementation
        class
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates user session_id and adds to session dictionary
            Return:
                - nrw session id
        """
        if user_id and type(user_id) is str:
            session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user id associated with passed session id
            Return:
                - user's id
        """
        if session_id and type(session_id) is str:
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get current user associated with specific session id
            Return:
                - User object for user instance whose user id is
                  linked to given session id
        """
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        current_user = User.get(user_id)
        return current_user

    def destroy_session(self, request=None) -> bool:
        """ Destroy session on logout
            Return:
                - True if session is destroy
                - False, otherwise
        """
        if not request:
            return False
        session_id = request.cookies.get(getenv('SESSION_NAME'))
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        SessionAuth.user_id_by_session_id.pop(session_id)
        return True