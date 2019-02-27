from flask import Blueprint, redirect, url_for, render_template, request, session, flash

from flask_dance.contrib.github import github
from . import db


blueprint = Blueprint("posts", __name__, url_prefix="/")


@blueprint.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    oauth_resp = resp.json()
    # TODO: Should be checking for errors from DB
    query = "INSERT INTO users (username, name, avatar, last_login) VALUES (%s, %s, %s, NOW()) ON CONFLICT (username) DO UPDATE SET last_login = NOW() RETURNING id"
    params = (
        oauth_resp["login"],
        oauth_resp.get("name", "") or "",
        oauth_resp.get("avatar_url", "") or "",
    )
    session["user_id"] = db.write(query, params, returning=True)

    users = db.read("SELECT COUNT(*) AS total FROM users", one=True)

    posts = db.read(
        "SELECT u.name AS name, u.username AS username, u.avatar AS avatar, p.message AS message, p.created AS created FROM posts AS p INNER JOIN users AS u ON p.author_id = u.id ORDER BY p.created DESC LIMIT 20"
    )

    return render_template(
        "index.html", login=oauth_resp["login"], total_users=users["total"], posts=posts
    )


@blueprint.route("/add", methods=["POST"])
def add_post():
    message = request.form.get("message")
    query = "INSERT INTO posts (author_id, message) VALUES (%s, %s)"
    params = (session["user_id"], message)
    db.write(query, params)
    flash("Successfully posted message", "success")
    return redirect(url_for("posts.index"))
