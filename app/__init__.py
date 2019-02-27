import os
from . import db
from flask import Flask, redirect, url_for, render_template

# This is for Heroku
from werkzeug.contrib.fixers import ProxyFix

# GitHub is the easiest to setup
from flask_dance.contrib.github import make_github_blueprint, github


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # TODO: what's the difference between these two lines?
    app.config.from_mapping(SECRET_KEY="dev")
    app.secret_key = "supersekrit12345"

    # For GitHub
    blueprint = make_github_blueprint(
        client_id=os.environ.get("GITHUB_CLIENT_ID"),
        client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    )
    app.register_blueprint(blueprint, url_prefix="/login")

    from . import posts
    app.register_blueprint(posts.blueprint)

    
    return app
