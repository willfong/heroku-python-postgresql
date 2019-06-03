from flask import Blueprint, redirect, url_for, render_template, request, session, flash

blueprint = Blueprint("index", __name__, url_prefix="/")


@blueprint.route("/")
def home():
    return render_template(
        "index.html"
    )
