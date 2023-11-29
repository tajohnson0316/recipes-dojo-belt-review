from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import recipe_model

bcrypt = Bcrypt(app)


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.list_of_recipes = []
        self.list_of_favorites = []


    """ -- CLASS METHODS -- """


    # CREATE one user
    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result


    # SELECT one user by ID
    @classmethod
    def get_one_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        return cls(result[0])


    # SELECT one user by email
    @classmethod
    def get_one_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s;
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        # if the resulting list is empty, return None
        if len(result) == 0:
            return None

        return cls(result[0])


    # SELECT one user by ID with a list of recipes they have favorited
    @classmethod
    def get_one_with_favorites(cls, data):
        query = """ 
        SELECT *
        FROM users u 
        LEFT JOIN favorites f ON f.user_id = u.id
        LEFT JOIN recipes r ON f.recipe_id = r.id
        WHERE u.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        current_user = cls(results[0])

        for row in results:
            if row["r.id"] is not None:
                new_favorite = {
                    "id": row["r.id"],
                    "name": row["name"],
                    "instructions": row["instructions"],
                    "description": row["description"],
                    "made_on": row["made_on"],
                    "under_30": row["under_30"],
                    "user_id": row["r.user_id"],
                    "created_at": row["r.created_at"],
                    "updated_at": row["r.updated_at"],
                }
                recipe = recipe_model.Recipe(new_favorite)
                recipe.user = cls.get_one_by_id({"id": row["r.user_id"]})
                current_user.list_of_favorites.append(recipe)
        return current_user


    # INSERT one recipe to the favorites list
    @classmethod
    def add_recipe_to_favorites(cls, data):
        query = """ 
        INSERT INTO favorites (user_id, recipe_id)
        VALUES (%(user_id)s, %(recipe_id)s);
        """

        new_favorite_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_favorite_id


    # DELETE one favorited recipe (unfavorite)
    @classmethod
    def delete_one_from_favorites(cls, data):
        query = """ 
        DELETE FROM favorites f
        WHERE f.user_id = %(user_id)s and f.recipe_id = %(recipe_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)


    """ -- STATIC METHODS -- """


    # User validation method
    @staticmethod
    def validate_registration(data):
        is_valid = True

        # Blank first name validation
        if len(data['first_name']) < 2:
            flash("Required field. Please provide a first name (min. 2 characters)", "error_first_name")
            is_valid = False
        # Blank last name validation
        if len(data['last_name']) < 2:
            flash("Required field. Please provide a last name (min. 2 characters)", "error_last_name")
            is_valid = False
        # Email validation via regex
        if not EMAIL_REGEX.match(data['email']):
            flash("Required field. Please provide a valid email", "error_email")
            is_valid = False
        # Non-unique email validation
        if User.get_one_by_email(data) is not None:
            flash("Account email already exists. Please try again", "error_email")
            is_valid = False
        # Blank password validation
        if len(data['password']) == 0:
            flash("Required field. Please provide a valid password", "error_password")
            is_valid = False
        # Password confirmation validation
        if data['password'] != data['confirm_password']:
            flash("Password mismatch. Please confirm both password fields match", "error_password")
            is_valid = False

        return is_valid


    # Login email validation method
    @staticmethod
    def validate_login_email(email):
        is_valid = True

        # Email validation via regex + check for an existing user/email pair
        if not EMAIL_REGEX.match(email):
            flash("Required field. Please provide a valid email address to log in", "error_login_email")
            is_valid = False
        elif User.get_one_by_email({'email': email}) is None:
            flash("No account found. Please check email and try again", "error_login_email")
            is_valid = False

        return is_valid


    # Login password validation
    @staticmethod
    def validate_password(hashed_password, unhashed_password):
        is_valid = True

        if len(unhashed_password) == 0:
            flash("Required field. Please provide a valid password to log in", "error_login_password")
            is_valid = False
        if not bcrypt.check_password_hash(hashed_password, unhashed_password):
            flash("Incorrect password. Please check password and try again", "error_login_password")
            is_valid = False

        return is_valid


    # Encrypt password
    @staticmethod
    def encrypt_string(text):
        return bcrypt.generate_password_hash(text)