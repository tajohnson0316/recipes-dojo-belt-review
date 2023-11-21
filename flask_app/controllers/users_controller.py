from flask import render_template  # request, redirect, session

from flask_app import app


@app.route("/", methods=["GET"])
def display_login_registration():
    return render_template("login_registration.html")