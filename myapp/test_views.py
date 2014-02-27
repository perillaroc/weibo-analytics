# encoding: utf-8
import json
from flask import request, url_for, render_template, g, redirect
from flask.ext.security import login_required, current_user

from flask.ext.security import login_required, current_user, login_user, logout_user

from myapp.models import User
from myapp import app, db

from weibo import APIClient
client = APIClient(app_key = app.config['APP_KEY'], \
        app_secret = app.config['APP_SECRET'], redirect_uri = app.config['CALLBACK_URL'])

@app.route('/test-get-weibo-list')
@login_required
def get_weibo_list():
    user = g.user
    print user.token
    token_1 = g.user.token#.decode("utf-8")
    token = json.loads(token_1)
    client.set_access_token(token['access_token'],token['expires'])
    results = client.statuses.user_timeline.get()
    print results
    return 'Hello World!'