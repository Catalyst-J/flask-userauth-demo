
# Standard Forms imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# Form Validators
# Data Required - field cannot be blank
# Email - checks if field follows the e-mail format
# EqualTo - allows double checking, such as 'Confirm Email' or 'Confirm Password'
# ValidationError - Returns error when something is invalid
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('E-mail ', validators=[DataRequired(message="Invalid e-mail address"), Email()])
    username = StringField('Username ', validators=[DataRequired()])
    
    # This has a password double checker, using the EqualTo('<variable_name>')
    password = PasswordField('Password ', validators=[DataRequired(), EqualTo('password_confirm', message="Passwords must match.")])
    password_confirm = PasswordField('Confirm Password ', validators=[DataRequired()])

    submit = SubmitField('Register')

    # This checks if the e-mail already exists in the database
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("E-mail already in use.")

    # This checks if the username already exists in the database
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is arleady taken.")

class LoginForm(FlaskForm):
    email = StringField('E-mail ', validators=[DataRequired(message="Invalid e-mail address"), Email()])
    password = PasswordField('Password ', validators=[DataRequired()])
    submit = SubmitField("Log In")
