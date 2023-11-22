from flask import render_template, request, redirect, session

from flask_app import app
from flask_app.models.user_model import User


@app.route("/", methods=["GET"])
def display_login_registration():
    return render_template("login_registration.html")


@app.route("/users/new", methods=['POST'])
def register_new_user():
    user_id = User.create_user(request.form)

    return redirect("/")