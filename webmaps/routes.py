from flask import render_template, url_for, flash, redirect, request
from webmaps import app, bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/home")
def home():
    return render_template("home.html", title='Home')


@app.route("/about")
def about():
    return render_template("about.html", title='About')
