from flask import Flask
from flask_bcrypt import Bcrypt

APP = Flask(__name__)
BCRYPT = Bcrypt(APP)
