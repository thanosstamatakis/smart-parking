""" This module contains all the web app urls. """
from flask import render_template, request
from app import APP


@APP.route("/")
def landing():
    print('Hello')
    return render_template("landing.html")


@APP.route("/home")
def home(request):
    return render_template("home.html", title='Home')


@APP.route("/about")
def about(request):
    return render_template("about.html", title='About')
