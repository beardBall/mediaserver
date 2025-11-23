import json
from functools import wraps
from flask import current_app, session, redirect, url_for, request


def load_users():
    users_file = current_app.config.get("USERS_FILE")
    if not users_file or not users_file.exists():
        return {}
    with open(users_file, "r", encoding="utf-8") as f:
        return json.load(f)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("main.login", next=request.path))
        return f(*args, **kwargs)

    return decorated
