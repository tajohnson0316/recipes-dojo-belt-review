from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt

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
        self.list_of_users = []


    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result


    # Get one by email
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


    # User validation method
    @staticmethod
    def validate_registration(data):
        is_valid = True

        # Blank first name validation
        if len(data['first_name']) == 0:
            flash("Required field. Please provide a first name", "error_first_name")
            is_valid = False
        # Blank last name validation
        if len(data['last_name']) == 0:
            flash("Required field. Please provide a last name", "error_last_name")
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


    # Encrypt password
    @staticmethod
    def encrypt_string(text):
        return bcrypt.generate_password_hash(text)