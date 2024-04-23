#!/usr/bin/env python3
"""A Simple Flask App
"""
from flask import (
    Flask, jsonify, request, abort, redirect, url_for
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
        A JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def create_user() -> str:
    """ POST /users
    Return:
        - A JSON payload with user information
        - 400 if email already registered
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Return:
        - A JSON payload with login information
        - 401 if email or password is invalid
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    Return:
        - 403 if session_id is invalid or user not found
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    Return:
        - A JSON payload with user information
        - 403 if session_id is invalid or user not found
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ POST /reset_password
    Return:
        - A JSON payload with password token information
        - 403 if email not found
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password():
    """ PUT /reset_password
    Return:
        - A JSON payload with password update information
        - 403 email or reset_token is invalid
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
