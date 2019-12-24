#!/usr/bin/env python

# ------------------------------------------------------------------------------
# app.py
# Author: Alan Ding
# ------------------------------------------------------------------------------

from sys import argv
from flask import Flask, request, make_response, redirect, render_template, \
    url_for
from stravalib import Client
import os
import requests

# ------------------------------------------------------------------------------

API_BASE_URL = 'https://www.strava.com/api/v3'
LEGENDS_OUT = '22248347'
LEGENDS_BACK = '22248349'

app = Flask(__name__, template_folder='./templates')

# ------------------------------------------------------------------------------

@app.before_request
def before_request():
    # redirect http to https
    if request.url[0:5] != 'https':
        return redirect(request.url.replace('http', 'https', 1))

@app.route('/login')
def login():
    return make_response(render_template('login.html'))

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))

    # delete authorization cookie
    response.set_cookie('authcookie', '', expires=0)

    return response

@app.route('/authorization')
def authorization():
    code = request.args.get('code')
    client = Client()
    token_response = client.exchange_code_for_token(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        code=code
    )

    access_token = token_response['access_token']

    client = Client(access_token=access_token)

    athlete = client.get_athlete()
    name = athlete.firstname + ' ' + athlete.lastname
    if name == 'Adam Chang':
        return redirect(url_for('not_legend'))

    r_out = requests.get(API_BASE_URL +
                         '/segments/' + LEGENDS_OUT + '/all_efforts' +
                         '?access_token=' + access_token)

    legends_out_data = r_out.json()

    r_back = requests.get(API_BASE_URL +
                          '/segments/' + LEGENDS_BACK + '/all_efforts' +
                          '?access_token=' + access_token)

    legends_back_data = r_back.json()

    if len(legends_out_data) == 0 or len(legends_back_data) == 0:
        return redirect(url_for('not_legend'))

    # user is authorized at this point
    response = redirect(url_for('chat'))
    response.set_cookie('name', name)
    response.set_cookie('authcookie', os.environ.get('VERIFICATION_KEY'))
    return response

@app.route('/not-legend')
def not_legend():
    html = render_template('not-eligible.html')
    return make_response(html)

@app.route('/')
@app.route('/index')
def index():
    if request.cookies.get('name') is not None:
        return redirect(url_for('chat'))

    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if request.cookies.get('authcookie') != os.environ.get('VERIFICATION_KEY'):
        return redirect(url_for('login'))

    name = request.cookies.get('name')

    return make_response(render_template('chat.html', name=name))

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)