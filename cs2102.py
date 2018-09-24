import os
from app import create_app, ItemForm, LoginForm, SignUpForm, login_manager
from flask_login import login_required, logout_user, login_user
import db
from models import user as UserModel
from werkzeug.security import generate_password_hash
from flask import render_template, redirect, url_for, g, flash, request
from datetime import datetime
import json

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@login_manager.user_loader
def load_user(user_id):
    """
    This method is called automatically by Flask-Login to get the user by his id whenever Flask-Login needs the User
    object.
    :param user_id:
    :return: User who's id his the given id
    """
    return UserModel.get_user_by_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route contains the login page and the login form. When submitted, we verify if the user exists in the database
    and his credentials are correct.
    :return:
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = UserModel.get_user_by_username(form.username.data)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # If the user wanted to access from a different page instead of the home page, we can keep track of
            # of this url so as to redirect the user back
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):  # check that the next_url is a relative URL
                next_url = url_for('index')
            return redirect(next_url)
        flash("Invalid username or password", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Use the Flask-Login's implementation of logout user.
    :return:
    """
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This route contains the sign up page and form. When submitted, we create the user in the database and redirect them
    to the login page for them to login immediately.
    :return:
    """
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = UserModel.User(None, form.username.data, form.name.data,
                              generate_password_hash(form.password.data), form.phonenumber.data)
        user.create_user()
        flash("You can now login", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', current_time=datetime.utcnow())
