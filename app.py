#!/usr/bin/env python

# ------------------------------------------------------------------------------
# app.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from sys import argv
from flask import Flask, request, make_response, redirect, render_template, \
    url_for
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user
import os
import requests
import json

# ------------------------------------------------------------------------------

API_BASE_URL = 'https://www.strava.com/api/v3'
LEGENDS_OUT = '22248347'
LEGENDS_BACK = '22248349'

# ------------------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY=os.environ['SESSION_KEY']
)

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

# helper function definitions
def get_access_details(auth_code):
    r = requests.post('https://www.strava.com/oauth/token' +
                      '?client_id=' + os.environ['CLIENT_ID'] +
                      '&client_secret=' + os.environ['CLIENT_SECRET'] +
                      '&code=' + auth_code +
                      '&grant_type=authorization_code')

    return r.json()

# ------------------------------------------------------------------------------

# site pages

@app.route('/login')
def login():
    html = render_template('login.html')
    return make_response(html)

@app.route('/exchange-token')
def check_eligibility():
    auth_code = request.args.get('code')
    print('****************request.args*******************: ' + str(request.args.items()))

    access_details = get_access_details(auth_code)
    access_token = access_details['access_token']
    user_id = access_details['athlete']['id']
    username = access_details['athlete']['firstname'] + ' ' + \
        access_details['athlete']['lastname']

    r_out = requests.get(API_BASE_URL +
                         '/segments/' + LEGENDS_OUT + '/all_efforts' +
                         '?access_token=' + access_token)

    legends_out_data = r_out.json()

    r_back = requests.get(API_BASE_URL +
                          '/segments/' + LEGENDS_BACK + '/all_efforts' +
                          '?access_token=' + access_token)

    legends_back_data = r_back.json()

    if len(legends_out_data) == 0 or len(legends_back_data) == 0:
        return redirect(url_for('not-legend'))
    else:
        user = User(user_id, username)
        login_user(user)
        return redirect(url_for('index'))

@app.route('/not-legend')
def not_legend():
    html = render_template('not-eligible.html')
    return make_response(html)

@app.route('/')
@app.route('/index')
@login_required
def index():
    html = render_template('index.html')
    return make_response(html)

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)