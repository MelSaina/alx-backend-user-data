#!/usr/bin/env python3
""" Module of Users views
"""
import os
from flask import (
    abort, jsonify, request, make_response
)

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login
    Form body:
      - email
      - password
    Return:
      - 200 User object JSON represented
      - 400 if either email and password are missing
      - 404 if a user with the email is not found
    """
    email, password = request.form.get('email'), request.form.get('password')
    if email is None or '':
        return jsonify({"error": "email missing"}), 400
    if password is None or '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if user == []:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    cookie_name = os.getenv('SESSION_NAME')
    session_id = auth.create_session(user[0].id)
    response = make_response(jsonify(user[0].to_json()))
    if cookie_name and session_id:
        response.set_cookie(cookie_name, session_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout(user_id: str = None) -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - 200 empty JSON is user session has been deleted and user logged out
      - 404 if request object has not session id
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)