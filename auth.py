from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from models import db, User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/chat")
    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        user = User(email=request.form["email"], password=hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect("/chat")
    return render_template("signup.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
