# encoding: utf-8
import json
import datetime
import string

from flask import request, g, jsonify

from flask.ext.security import login_required

from myapp.models import User, WeiboList
from myapp import app, db
from myapp.api_app import api_app

from weibo import APIClient

client = APIClient(app_key=app.config['APP_KEY'],
                   app_secret=app.config['APP_SECRET'],
                   redirect_uri=app.config['CALLBACK_URL'])

@api_app.route('/statistic/status-count')
@login_required
def get_status_count():
    default_start_date = datetime.date.today()
    default_end_date = default_start_date - datetime.timedelta(days=30)
    start_date = request.args.get('start_date', default_start_date.strftime("%Y-%m-%d"))
    end_date = request.args.get('end_date', default_end_date.strftime("%Y-%m-%d"))
    time_interval = request.args.get('time_interval', 'day')
    result = {
        "start_date": start_date,
        "end_date": end_date,
        "time_interval": time_interval
    }
    return jsonify(result)
