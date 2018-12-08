""" This module contains all the web app urls. """
from flask import render_template, request
from webmaps import APP


@APP.route("/")
def landing():
    print('Hello')
    return render_template("landing.html")


@APP.route("/home")
def home():
    return render_template("home.html", title='Home')


@APP.route("/about")
def about():
    return render_template("about.html", title='About')


@APP.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404
