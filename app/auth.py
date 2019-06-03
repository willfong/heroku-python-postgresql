import os
from flask import Blueprint, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github


blueprint = Blueprint("auth", __name__, url_prefix="/auth")
login_github = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
)


def login_required(func):
    def wrapper():
        if not github.authorized:
            return redirect(url_for("github.login"))
        return func()

    return wrapper
