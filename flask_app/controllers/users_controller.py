from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


""" -- GET routes """


# Index
@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
@app.route("/register", methods=["GET"])
def display_login_registration():
    return render_template("login_registration.html")


# Display homepage
@app.route("/home", methods=["GET"])
def display_homepage():
    if "user_id" not in session:
        return redirect("/")

    current_user = User.get_one_with_favorites({"id": session["user_id"]})

    list_of_favorites = current_user.list_of_favorites
    list_of_recipes = Recipe.get_all()

    # Iterate through the user's list favorite recipes, removing each one from the general list of all recipes
    # This ensures there are no duplicate recipes between the two lists that get rendered
    for favorite in list_of_favorites:
        for recipe in list_of_recipes:
            if recipe.name == favorite.name:
                list_of_recipes.remove(recipe)

    return render_template(
        "recipes_home.html",
        current_user=current_user,
        list_of_recipes=list_of_recipes,
    )


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


# User log out
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


# Add a recipe to the user's list of favorites
@app.route("/users/<int:recipe_id>/favorites/add", methods=["POST"])
def add_to_favorites(recipe_id):
    User.add_recipe_to_favorites(
        {"user_id": session["user_id"], "recipe_id": recipe_id}
    )

    return redirect("/home")


# Remove a recipe from the user's list of favorites
@app.route("/users/<int:recipe_id>/favorites/remove", methods=["POST"])
def remove_from_favorites(recipe_id):
    User.delete_one_from_favorites(
        {"user_id": session["user_id"], "recipe_id": recipe_id}
    )

    return redirect("/home")