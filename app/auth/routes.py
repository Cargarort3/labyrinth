from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .services import AuthService
from app.publication.services import PublicationService

auth = Blueprint("auth", __name__, template_folder="templates")

publicationService = PublicationService()
authService = AuthService()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (3 <= len(username) <= 20) or not (8 <= len(password) <= 20):
            return "Username or password doesn't meet the required length.", 400

        user = authService.register_user(username, password)
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

        user = authService.authenticate_user(username, password)
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


@auth.route('/profile', methods=['GET'])
@login_required
def get_my_profile():
    publications = publicationService.get_user_publications(current_user.id)
    return render_template('my_profile.html', publications=publications)


@auth.route('/profile/<int:id>', methods=['GET'])
def get_user_profile(id):
    user = authService.get_user_by_id(id)
    if not user:
        return "User not found", 404
    if user == current_user:
        return render_template('my_profile.html')
    publications = publicationService.get_user_publications(user.id)
    return render_template('user_profile.html', user=user, publications=publications)
