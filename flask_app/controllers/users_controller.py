from flask import render_template, request, redirect, session

from flask_app import app
from flask_app.models.user_model import User


@app.route("/", methods=["GET"])
def display_login_registration():
    return render_template("login_registration.html")


@app.route("/users/new", methods=['POST'])
def register_new_user():
    # call User's static method to validate user registration
    if not User.validate_registration(request.form):
        # redirect back to registration page in case of invalid registration
        return redirect("/")

    user_id = User.create_user(request.form)

    return redirect("/")