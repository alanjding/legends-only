#!/usr/bin/env python

# ------------------------------------------------------------------------------
# app.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from sys import argv
from database import Database
from flask import Flask, request, make_response, redirect, render_template
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import os

# ------------------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

# Fix performance hits from default config (see StackOverflow post on this)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Populates DATABASE_URL environment variable
heroku = Heroku(app)
database_url = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

# ------------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
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