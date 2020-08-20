
# Simply imports the Database and Login Manager from the __init__.py
from project import db, login_manager

# We'll be using Werkzeug to handle the hashing and checking of it.
from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin is a class that allows the developer to use
# additional features, when managing users and such.
from flask_login import UserMixin

# This loads the current user so that we can display certain
# views depending on who they are.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create a User Model
class User(db.Model, UserMixin):
    
    # Table Name (optional, by default uses the class name)
    __tablename__ = 'users'

    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # Allows instantiation of a row
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    # Checks the password if correct or not.
    # Returns boolean, True or False.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)