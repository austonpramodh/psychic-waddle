from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask import render_template
from models import db, User
import re


# Initialization section -----------------
app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file_path = os.path.join(project_dir, "ecomm.db")
database_file = "sqlite:///{}".format(database_file_path)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'session_secret!!'
# Initialize the database
db.init_app(app)

# Check if db file exists, else create one
database_file_exists = os.path.exists(database_file_path)
if database_file_exists:
    print("Using existing db file!")
else:
    print("Creating a db file!!")
    with app.app_context():
        db.create_all()

# Initialization section -----------------

# Actual routes!!


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = User.query.filter_by(
            username=username,
            password=password).first()

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account already exists
        existing_username = User.query.filter_by(
            username=f'{username}').first()
        existing_user_email = User.query.filter_by(
            username=f'{username}').first()

        if existing_user_email:
            msg = 'Account already exists !'
        elif existing_username:
            msg = "Username is already taken!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            # Create the user
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)
