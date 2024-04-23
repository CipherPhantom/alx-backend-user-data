#!/usr/bin/env python3
"""End-to-end integration test"""
import requests

URL = "http://127.0.0.1:5000{}"


def register_user(email: str, password: str) -> None:
    """Registers a new user"""
    data = {"email": email, "password": password}
    response = requests.post(URL.format('/users'), data=data)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Logs in with wrong password"""
    data = {"email": email, "password": password}
    response = requests.post(URL.format('/sessions'), data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Logs in with valid information"""
    data = {"email": email, "password": password}
    response = requests.post(URL.format('/sessions'), data=data)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Get profile without logging in"""
    response = requests.get(URL.format('/profile'))
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Get profile after logging in"""
    cookies = {"session_id": session_id}
    response = requests.get(URL.format('/profile'), cookies=cookies)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """Logs out"""
    cookies = {"session_id": session_id}
    response = requests.delete(
        URL.format('/sessions'), cookies=cookies, allow_redirects=True)
    assert response.url == URL.format('/')
    assert response.status_code == 200
    assert response.history != []
    assert response.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """Gets a reset password token"""
    data = {"email": email}
    response = requests.post(URL.format('/reset_password'), data=data)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert "email" in response.json()
    assert "reset_token" in response.json()
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates the user's password"""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(URL.format('/reset_password'), data=data)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
