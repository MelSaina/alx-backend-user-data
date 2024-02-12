#!/usr/bin/env python3from typing import Optional, Tuple, TypeVar

"""
Basic authentication module
"""
import binascii
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Optional, Tuple, TypeVar


class BasicAuth(Auth):
    """ Basic authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) \
            -> Optional[str]:
        """ Retrieves authentication parameters form authorization header
            Returns:
             - Base64 part of authorization header
        """
        if authorization_header is None or \
            type(authorization_header) is not str or \
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> Optional[str]:
        """ Decodes base64 authorization string
            Returns:
                - Decoded base64 authentication string
        """
        if not base64_authorization_header or \
                type(base64_authorization_header) is not str:
            return None
        try:
            auth_str = b64decode(base64_authorization_header, validate=True)
        except binascii.Error:
            return None
        else:
            return auth_str.decode('utf-8')

    def extract_user_credentials(self,
                                 decode_base64_authorization_header: str) \
            -> Tuple[Optional[str], Optional[str]]:
        """ Extract user credential
            Return:
                - username
                - password
        """
        if not decode_base64_authorization_header or \
                type(decode_base64_authorization_header) is not str or \
                ":" not in decode_base64_authorization_header:
            return None, None
        email, pwd = decode_base64_authorization_header.split(":", maxsplit=1)
        return email, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """ Creates user object based on
            Return:
                - User object if credentials are valid
                - None otherwise
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None

        try:
            users = User.search(attributes={"email": user_email})
        # Exception from passing unknown s_class to DATA
        # Check module base.py lines 12 and 125-137(instance method
        # 'search')
        except KeyError:
            return None

        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates credentials passed in 'Authorization' header'
            Returns:
                - User object associated with valid credentials
        """
        auth_header = self.authorization_header(request)
        b64_str = self.extract_base64_authorization_header(auth_header)
        decode_b64_str = self.decode_base64_authorization_header(b64_str)
        email, pwd = self.extract_user_credentials(decode_b64_str)
        user = self.user_object_from_credentials(email, pwd)
        return user