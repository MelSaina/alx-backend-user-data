#!/usr/bin/env python3
""" Password encryption module """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Creates hashed password """
    pwd = password.encode()
    hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if hashed password matches
        unhashed password
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False