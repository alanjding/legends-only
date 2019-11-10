#!/usr/bin/env python

# ------------------------------------------------------------------------------
# app.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from sys import argv
from flask import Flask, request, make_response, redirect, render_template
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user
import os

# ------------------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

# Fix performance hits from default config (see StackOverflow post on this)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Populates DATABASE_URL environment variable
heroku = Heroku(app)
database_url = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ------------------------------------------------------------------------------

# defines a user
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id # Strava athlete id
        self.name = name # Strava name

    def __repr__(self):
        return "%d/%s" % (self.id, self.auth_code)

# ------------------------------------------------------------------------------

@app.route('/login')
def login():
    auth_code = request.args.get('a')

    html = render_template('login.html')
    response = make_response(html)
    return response


@app.route('/')
@app.route('/index')
@login_required
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)