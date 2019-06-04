import os
from flask import Blueprint, redirect, url_for, flash, session, render_template
from flask_dance.contrib.github import make_github_blueprint, github
from . import db

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

login_github = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    redirect_to="auth.oauth_github"
)


# TODO: Don't know why my decorator doesn't work.
def login_required(func):
    def wrapper():
        print("Starting login_required")
        if 'user_id' not in session:
            return redirect(url_for("auth.login"))
        print("Already logged in...")
        return func()

    return wrapper


@blueprint.route("/login")
def login():
    return render_template("login.html")


@blueprint.route("/oauth/github")
def oauth_github():
    resp = github.get("/user")
    assert resp.ok
    oauth_resp = resp.json()
    # TODO: Should be checking for errors from DB
    query = "INSERT INTO users (username, name, avatar, last_login) VALUES (%s, %s, %s, NOW()) ON CONFLICT (username) DO UPDATE SET last_login = NOW() RETURNING id"
    # GitHub/Oauth returns keys with values of None. Can't use .get() defaults, need to use or.
    params = (
        oauth_resp["login"],
        oauth_resp.get("name", "") or "",
        oauth_resp.get("avatar_url", "") or "",
    )
    session["user_id"] = db.write(query, params, returning=True)
    flash("Successfully logged in via GitHub!", "success")
    return redirect(url_for("app.home"))


@blueprint.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("index.home"))

