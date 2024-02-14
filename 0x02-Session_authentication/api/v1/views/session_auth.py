#!/usr/bin/env python3
""" Session authentication route module
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ Session authentication route
        POST parameters:
            - email: user's email
            - password: user's password
        Returns - response with user details and session cookie
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    current_user = None
    for user in users:
        if user.is_valid_password(pwd):
            current_user = user
            break
    if not current_user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()), 200)
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ Logs out user and destroys session
        User needs to be logged in with a session
        id associated with their user_id
    """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if not status:
        abort(404)
    return jsonify({}), 200