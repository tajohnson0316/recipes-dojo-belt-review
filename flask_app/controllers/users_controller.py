from flask import render_template, request, redirect, session

from flask_app import app
from flask_app.models.user_model import User


""" -- GET routes """


# Index route
@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
@app.route("/register", methods=["GET"])
def display_login_registration():
    return render_template("login_registration.html")


""" -- POST routes """


# User registration
@app.route("/users/register", methods=['POST'])
def register_new_user():
    # call User's static method to validate user registration
    if not User.validate_registration(request.form):
        # redirect back to registration page in case of invalid registration
        return redirect("/")

    # Assign the retrieved user's ID to the session's
    session['user_id'] = User.create_user(
        {
            **request.form,
            'password': User.encrypt_string(request.form['password'])
        }
    )

    return redirect("/home")


# User login
@app.route("/users/login", methods=["POST"])
def login():
    email = request.form['login_email']

    # Login email validation
    if not User.validate_login_email(email):
        return redirect("/")

    user = User.get_one_by_email({'email': email})

    # Login password validation
    if not User.validate_password(user.password, request.form['login_password']):
        return redirect("/")

    session['user_id'] = user.id

    return redirect("/home")


# Log out
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")