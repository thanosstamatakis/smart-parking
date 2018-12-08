""" This module contains all the web app urls. """
from flask import render_template, request
from webmaps import APP
import folium


@APP.route("/")
def landing():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium_map.save('webmaps/templates/map.html')
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
