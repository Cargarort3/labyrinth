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

        user = AuthService.register_user(username, password)
        print(user)
        if user:
            return redirect(url_for('auth.login'))
        return render_template("register.html", error="Username already taken")

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
        return render_template("login.html", error="Invalid credentials")

    return render_template('login.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
