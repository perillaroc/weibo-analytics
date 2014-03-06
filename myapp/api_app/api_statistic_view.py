# encoding: utf-8
import json
import datetime
import string

from flask import request, g, jsonify

from flask.ext.security import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func

from myapp.models import User, WeiboList,Calendar
from myapp import app, db
from myapp.api_app import api_app

from weibo import APIClient

client = APIClient(app_key=app.config['APP_KEY'],
                   app_secret=app.config['APP_SECRET'],
                   redirect_uri=app.config['CALLBACK_URL'])


@api_app.route('/statistic/status-count')
@login_required
def get_status_count():
    """
    SQL Statement For Day:
        SELECT `c`.`date` AS date,
        COUNT(`l`.`id`) AS count
        FROM (
            SELECT date as date
            FROM calendar
            WHERE date>='2014-02-01'
            AND date<='2014-02-28'
        )AS c
        LEFT JOIN weibo_list AS l
        ON DATE(l.created_at) = `c`.`date`
        GROUP BY date
        ORDER BY date
    """
    default_end_date = datetime.date.today()
    default_start_date = default_end_date - datetime.timedelta(days=30)
    start_date = request.args.get('start_date', default_start_date.strftime("%Y-%m-%d"))
    end_date = request.args.get('end_date', default_end_date.strftime("%Y-%m-%d"))
    time_interval = request.args.get('time_interval', 'day')

    date_list_query = db.session.query(Calendar.date.label("date")).\
        filter(Calendar.date >= start_date).\
        filter(Calendar.date <= end_date).\
        subquery()

    list_by_day = db.session.query(date_list_query.c.date, func.count(WeiboList.id).label("counts")).\
        outerjoin(WeiboList, date_list_query.c.date == func.DATE(WeiboList.created_at)).\
        group_by(date_list_query.c.date).\
        order_by(date_list_query.c.date).all()

    record_list = []
    for one_record in list_by_day:
        record_list.append({
            "date": one_record[0].strftime("%Y-%m-%d"),
            "counts": one_record[1]
        })

    result = {
        "start_date": start_date,
        "end_date": end_date,
        "time_interval": time_interval,
        "record":record_list
    }

    return jsonify(result)
