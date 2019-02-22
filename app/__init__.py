import os

from flask import Flask, redirect, url_for

# This is for Heroku
from werkzeug.contrib.fixers import ProxyFix

# GitHub is the easiest to setup 
from flask_dance.contrib.github import make_github_blueprint, github


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    
    # TODO: what's the difference between these two lines?
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.secret_key = "supersekrit12345"

    # For GitHub
    blueprint = make_github_blueprint(
        client_id=os.environ.get("GITHUB_CLIENT_ID"),
        client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    )
    app.register_blueprint(blueprint, url_prefix="/login")
    

    @app.route("/")
    def index():
        if not github.authorized:
            return redirect(url_for("github.login"))
        resp = github.get("/user")
        assert resp.ok
        return "You are @{login} on GitHub".format(login=resp.json()["login"])


    from . import db
    db.init_app(app)

    return app
