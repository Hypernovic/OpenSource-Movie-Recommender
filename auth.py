from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    userName = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(userName=userName).first()
    print(userName,password)
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    username = request.form.get('username')
    password = request.form.get('password')
    print(username,password)
    user = User.query.filter_by(userName=username).first()

    if user: # try again  
        flash('Username address already exists')
        return redirect(url_for('auth.signup'))

    # create new user Hash the password
    picture="https://api.dicebear.com/5.x/bottts/svg?seed="+username
    new_user = User(userName=username, password=generate_password_hash(password, method='sha256'), pic=picture)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))