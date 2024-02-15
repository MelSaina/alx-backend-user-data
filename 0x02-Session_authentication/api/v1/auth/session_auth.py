#!/usr/bin/env python3
"""
Defines a SessionAuth class that inherits from Auth class
"""
import uuid
from typing import (
    TypeVar,
    Union
)
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Authentication class implementation
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """
        Create session id from random string
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(
        self, session_id: str = None
    ) -> Union[str, None]:
        """
        Get user id from given session id
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> Union[TypeVar('User'), None]:
        """
        Holds the current authenticated logged in user
        """
        User.load_from_file()
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request))
        )

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout
        """
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