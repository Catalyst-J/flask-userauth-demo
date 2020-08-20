# Import the app and db instances
from project import app, db

# request - Local Proxy
# abort - to be able to raise HTTP exceptions such as 404 Not Found and etc.
from flask import render_template, redirect, request, url_for, flash, abort

# Import decorators from Flask-Login for the login_user page,
# pages that requires log-in (login_required), and logout_user
# for logging out the user.
from flask_login import login_user, login_required, logout_user

# Import the rest of the Models and Forms
from project.models import User
from project.forms import LoginForm, RegistrationForm

# A simple root page.
@app.route('/')
def home():
    return render_template('home.html')

# Adding @login_required will require the visitor to be logged in, 
# in order to access the page.
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# This simply logs out the user
@app.route('/logout')
@login_required
def logout():
    # The library handles the logging out of the user for us.
    logout_user()
    flash("You've been logged out.")

    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    # ! Warning: This returns an Error Code 500
    # !          Server Internal Error if user does not exist.

    form = LoginForm()
    
    if form.validate_on_submit():

        # Queries the database for the user in the database,
        # will return data but if it doesn't exist then None.
        user = User.query.filter_by(email=form.email.data).first()

        # Checks if the user supplied a password and that it's correct.
        if user.check_password(form.password.data) and user is not None:
            
            # Log-in the user
            login_user(user)
            flash("Logged in successfully!")

            # Grabs the request and places it on 'next'.
            # For example, if a client tries to access the dashboard
            # without being logged in then they will be redirected to
            # the log-in page.
            #
            # The purpose this serves is to automatically redirect the
            # user to the recently attempted-to-access View when they're
            # logged in successfully.
            next = request.args.get('next')
            
            # This checks if 'next' has something in it
            if next == None or not next[0] == '/':
                # This redirects client to the Dashboard.
                next = url_for('dashboard')

            # When 'next' has data, redirect to it.
            # So if the client attempted to access Dashboard (example)
            # without being logged in, then this code redirects
            # the client automatically.
            return redirect(next)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # This part of the code simply registers the new user.
    
    # No complicated checker here, since it's mostly done already
    # in the Forms itself using the validators.
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully!")

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)