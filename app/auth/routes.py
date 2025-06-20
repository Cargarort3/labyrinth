from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .services import AuthService

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (3 <= len(username) <= 20) or not (8 <= len(password) <= 20):
            return "Username or password doesn't meet the required length.", 400

        user = AuthService.register_user(username, password)
        if user:
            return redirect(url_for('auth.login'))
        return render_template("register.html", error="Username already taken"), 409

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = AuthService.authenticate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
        return render_template("login.html", error="Invalid credentials"), 401

    return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
