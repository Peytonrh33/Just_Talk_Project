from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, name, email, password) VALUES (%(username)s, %(name)s, %(email)s, %(password)s)"
        return connectToMySQL('personal_project_schema').query_db( query, data)
    
    @classmethod
    def get_user_id(cls, data):
        query = "SELECT * FROM users WHERE users.id=%(id)s;"
        results =  connectToMySQL('personal_project_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_email(cls,data):
        query = "SELECT * FROM users WHERE users.email=%(email)s;"
        results =  connectToMySQL('personal_project_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(data):

        is_valid = True

        if len(data['username']) < 2:
            is_valid = False
            flash("Username Required!")

        if len(data['name']) < 2:
            is_valid = False
            flash("Name Required!")

        if len(data['email']) < 2:
            is_valid = False
            flash("Email Required!")
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid email address!")
        else:
            # cannot say data here because of the data above, this is checking if email is repeated
            data_for_email = {
                'email': data['email']
            }
            potential_email = User.get_user_email(data_for_email)
            if potential_email:
                is_valid = False
                flash("Email already taken")

        if len(data['password']) < 8:
            is_valid = False
            flash("Password Required!")

        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("Passwords don't match!")

        return is_valid