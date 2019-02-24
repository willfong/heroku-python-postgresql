from flask import (
    Blueprint, redirect, url_for, render_template
)

from flask_dance.contrib.github import github
from . import db


blueprint = Blueprint('posts', __name__, url_prefix='/')

@blueprint.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    oauth_resp = resp.json()
    db.write(
        "INSERT INTO users (username, name, avatar, last_login) VALUES (%s, %s, %s, NOW()) ON CONFLICT (username) DO UPDATE SET last_login = NOW()",
        (oauth_resp["login"], oauth_resp["name"], oauth_resp["avatar_url"]),
    )
    users = db.read("SELECT COUNT(*) AS total FROM users")
    return render_template('index.html', login=oauth_resp["login"], total_users=users["total"])

@blueprint.route("/add", methods=["POST"])
def add_post():
    
