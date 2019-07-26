import os
from flask import Blueprint, redirect, url_for, flash, session, render_template
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from . import db

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

login_github = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    redirect_to="auth.oauth_github"
)

login_google = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    redirect_to="auth.oauth_google"
)

login_facebook = make_facebook_blueprint(
    client_id=os.environ.get("FACEBOOK_CLIENT_ID"),
    client_secret=os.environ.get("FACEBOOK_CLIENT_SECRET"),
    redirect_to="auth.oauth_facebook"
)


# TODO: Don't know why my decorator doesn't work.
def login_required(func):
    def wrapper():
        if 'user_id' not in session:
            return redirect(url_for("auth.login"))
        return func()

    return wrapper


@blueprint.route("/login")
def login():
    return render_template("login.html", loginpage=True)


@blueprint.route("/oauth/github")
def oauth_github():
    resp = github.get("/user")
    assert resp.ok
    oauth_resp = resp.json()
    print("GitHub Response:\n{}".format(oauth_resp))
    # TODO: Should be checking for errors from DB
    query = "INSERT INTO users (github_id, name, avatar, last_login) VALUES (%s, %s, %s, NOW()) ON CONFLICT (github_id) DO UPDATE SET last_login = NOW() RETURNING id, name"
    # GitHub/Oauth returns keys with values of None. Can't use .get() defaults, need to use or.
    params = (
        oauth_resp.get("id"),
        oauth_resp.get("name", "") or "",
        oauth_resp.get("avatar_url", "") or "",
    )
    session["user_id"], session["user_name"] = db.write(query, params, returning=True)
    flash("Successfully logged in via GitHub!", "success")
    return redirect(url_for("app.home"))


@blueprint.route("/oauth/google")
def oauth_google():
    resp = google.get("/plus/v1/people/me")
    oauth_resp = resp.json()
    print("Google Response:\n{}".format(oauth_resp))
    # TODO: Should be checking for errors from DB
    query = "INSERT INTO users (google_id, name, avatar, last_login) VALUES (%s, %s, %s, NOW()) ON CONFLICT (google_id) DO UPDATE SET last_login = NOW() RETURNING id, name"
    params = (
        oauth_resp.get("id"),
        oauth_resp.get("displayName", "") or "",
        oauth_resp.get("image", "").get("url").replace('/s50/', '/s500/') or "",
    )
    session["user_id"], session["user_name"] = db.write(query, params, returning=True)
    flash("Successfully logged in via Google!", "success")
    return redirect(url_for("app.home"))


@blueprint.route("/oauth/facebook")
def oauth_facebook():
    resp = facebook.get("/me")
    assert resp.ok
    oauth_resp = resp.json()
    print("Facebook Response:\n{}".format(oauth_resp))
    # TODO: Should be checking for errors from DB
    query = "INSERT INTO users (facebook_id, name, last_login) VALUES (%s, %s, NOW()) ON CONFLICT (facebook_id) DO UPDATE SET last_login = NOW() RETURNING id, name"
    params = (
        oauth_resp.get("id"),
        oauth_resp.get("name", "") or ""
    )
    session["user_id"], session["user_name"] = db.write(query, params, returning=True)
    flash("Successfully logged in via Facebook!", "success")
    return redirect(url_for("app.home"))


@blueprint.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("index.home"))

