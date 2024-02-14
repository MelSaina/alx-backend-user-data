#!/usr/bin/env python3
""" DocIn_it_In_it
"""
from flask import Blueprint
from models.user_session import UserSession


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *
from api.v1.auth.session_db_auth import SessionDBAuth

# Reloading users
User.load_from_file()

# Reloading sessions
UserSession.load_from_file()
try:
    for session in UserSession.all():
        SessionDBAuth.user_id_by_session_id[session.id] = session.user_id
except KeyError:
    pass
