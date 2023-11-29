from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.controllers import users_controller
from flask_app.models import user_model


""" -- GET ROUTES -- """


# Display the new recipe form
@app.route("/recipes/new/form", methods=["GET"])
def display_new_recipe_form():
    if "user_id" not in session:
        return redirect("/")

    return render_template("new_recipe_form.html")


# READ and display a recipe
@app.route("/recipes/<int:recipe_id>/view", methods=["GET"])
def display_recipe(recipe_id):
    current_user = user_model.User.get_one_by_id({"id": session["user_id"]})
    current_recipe = Recipe.get_one_with_favorites({"id": recipe_id})

    list_of_favorites = current_recipe.list_of_favorites
    favorites_length = len(list_of_favorites)

    return render_template(
        "display_recipe.html",
        current_user=current_user,
        current_recipe=current_recipe,
        list_of_favorites=list_of_favorites,
        favorites_length=favorites_length,
    )


# Display the edit recipe form
@app.route("/recipes/<int:recipe_id>/edit", methods=["GET"])
def display_edit_recipe_form(recipe_id):
    current_recipe = Recipe.get_one_by_id({"id": recipe_id})
    return render_template("edit_recipe_form.html", current_recipe=current_recipe)


""" -- POST ROUTES -- """


# CREATE a new recipe
@app.route("/recipes/add/new", methods=["POST"])
def add_new_recipe():
    if "user_id" not in session:
        return redirect("/")

    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new/form")

    new_recipe_id = Recipe.create_one({**request.form, "user_id": session["user_id"]})

    if request.form["add_favorite"] == "Yes":
        user_model.User.add_recipe_to_favorites(
            {"user_id": session["user_id"], "recipe_id": new_recipe_id}
        )

    return redirect("/home")


""" -- UPDATE ROUTES -- """


# UPDATE a recipe
@app.route("/recipes/<int:recipe_id>/edit/submit", methods=["POST"])
def update_recipe(recipe_id):
    Recipe.update_one_by_id({**request.form, "id": recipe_id})
    return redirect(f"/recipes/{recipe_id}/view")


""" -- DELETE ROUTES -- """


# DELETE a recipe by ID
@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/")

    Recipe.delete_one_by_id({"id": recipe_id})

    return redirect("/home")