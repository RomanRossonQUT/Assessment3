from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm  # Importing necessary forms
from flask_login import login_user, login_required, logout_user  # Importing login-related functions
from flask_bcrypt import generate_password_hash, check_password_hash  # Importing password hashing functions
from .models import User  # Importing the User model
from . import db  # Importing the database

# Creating a Blueprint for authentication routes
authbp = Blueprint('auth', __name__)

# Route for user registration
@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()  # Creating an instance of the RegisterForm
    if register.validate_on_submit():  # Checking if the form is validated
        uname = register.username.data  # Extracting username from the form
        pwd = register.password.data  # Extracting password from the form
        email = register.email.data  # Extracting email from the form
        user = db.session.scalar(db.select(User).where(User.name == uname))  # Querying the database for existing user
        if user:
            flash('Username already exists, please try another')  # Flashing a message if the username already exists
            return redirect(url_for('auth.register'))  # Redirecting to the registration page
        pwd_hash = generate_password_hash(pwd)  # Generating a hash of the password
        new_user = User(name=uname, password=pwd_hash, email=email)  # Creating a new User object
        db.session.add(new_user)  # Adding the new user to the session
        db.session.commit()  # Committing the changes to the database
        return redirect(url_for('main.index'))  # Redirecting to the main page after successful registration
    else:
        return render_template('register.html', form=register, heading='Register')  # Rendering the registration template

# Route for user login
@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()  # Creating an instance of the LoginForm
    error = None  # Initializing an error variable
    if login_form.validate_on_submit():  # Checking if the form is validated
        username = login_form.username.data  # Extracting username from the form
        password = login_form.password.data  # Extracting password from the form
        user = db.session.scalar(db.select(User).where(User.username == username))  # Querying the database for the user
        if user is None:
            error = 'Incorrect username'  # Setting an error message for an incorrect username
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'  # Setting an error message for an incorrect password
        if error is None:
            login_user(user)  # Logging in the user
            return redirect(url_for('main.index'))  # Redirecting to the main page after successful login
        else:
            flash(error)  # Flashing the error message
    return render_template('login.html', form=login_form, heading='Login')  # Rendering the login template

# Route for user logout
@authbp.route('/logout')
@login_required  # Requiring the user to be logged in to access this route
def logout():
    logout_user()  # Logging out the user
    return redirect(url_for('main.index'))  # Redirecting to the main page after logout
