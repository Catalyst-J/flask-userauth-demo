# Import OS for base directory checking
import os

# Import Flask libraries used in earlier lectures
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import Flask-Login to use as the Login Manager
from flask_login import LoginManager

# Instantiate the LoginManager()
login_manager = LoginManager()

# Setup standard Flask setup, Forms setup, and Database setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# Instantiate the LoginManager into the app
login_manager.init_app(app)

# This sets the default view when the user is logged
# In this case, user is redirected to the 'login' view to be set in the app.py
login_manager.login_view = 'login'
