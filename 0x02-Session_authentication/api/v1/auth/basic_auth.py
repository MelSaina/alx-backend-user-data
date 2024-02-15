#!/usr/bin/env python3
"""
Defines a BasicAuth class that inherits from Auth class
"""
import base64
from typing import Tuple, TypeVar, Union

from api.v1.auth.auth import Auth
from api.v1.views.users import User


class BasicAuth(Auth):
    """
    Basic Authentication class implementation
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extract Authorization header value
        """
        if (
            authorization_header is None
            or type(authorization_header) != str
            or not authorization_header.startswith('Basic ')
        ):
            return None
        return ''.join(authorization_header.split('Basic ')[1:])

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Base64 encode authorization_header
        """
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) != str
        ):
            return None
        try:
            encoded = base64.b64decode(base64_authorization_header)
            return encoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str]:
        """
        Extract email username and password
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) != str
            or ":" not in decoded_base64_authorization_header
        ):
            return None, None
        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], ':'.join(credentials[1:])

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Union[TypeVar('User'), None]:
        """
        Gets the User instance based on given email and password
        """
        if (
            user_email is None or type(user_email) != str
            or user_pwd is None or type(user_pwd) != str
        ):
            return None
        User.load_from_file()
        if User.count() > 0:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Loads the current_user object
        """
        email, password = self.extract_user_credentials(
            self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(
                    self.authorization_header(request=request)))
        )
        return self.user_object_from_credentials(email, password)