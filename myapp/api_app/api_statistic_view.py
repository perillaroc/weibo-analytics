# encoding: utf-8
import json
import datetime
import calendar

from flask import request, g, jsonify

from flask.ext.security import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct, and_

from myapp.models import User, WeiboList, Calendar
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

    start_date = request.args.get('start_date', '')
    if start_date == '':
        start_date = default_start_date
    else:
        start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_datetime.date()

    end_date = request.args.get('end_date', '')
    if end_date == '':
        end_date = default_end_date
    else:
        end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_datetime.date()

    time_interval = request.args.get('time_interval', 'day')

    record_list = []

    if time_interval == "day":
        date_list_query = db.session.query(Calendar.date.label("date")). \
            filter(Calendar.date >= start_date.isoformat()). \
            filter(Calendar.date <= end_date.isoformat()). \
            subquery()

        list_by_day = db.session.query(date_list_query.c.date, func.count(WeiboList.id).label("counts")). \
            outerjoin(WeiboList, date_list_query.c.date == func.DATE(WeiboList.created_at)). \
            group_by(date_list_query.c.date). \
            order_by(date_list_query.c.date).all()

        for one_record in list_by_day:
            record_list.append({
                "date": one_record[0].isoformat(),
                "count": one_record[1]
            })

        result = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "time_interval": time_interval,
            "record": record_list
        }

    elif time_interval == "month":
        #TODO 2014.03.09 perillaroc: Use sql script below
        # SELECT MONTH(`c`.`date`) AS d,
        # COUNT(`l`.`id`) AS count
        # FROM (
        #             SELECT date as date
        #             FROM calendar
        #             WHERE date>='2014-01-01'
        #             AND date<='2014-03-28'
        # )AS c
        # LEFT JOIN weibo_list AS l
        # ON DATE(l.created_at) = `c`.`date`
        # GROUP BY d
        # ORDER BY d
        first_day_of_start_month = datetime.date(start_date.year, start_date.month, 1)
        first_day_of_end_month = datetime.date(end_date.year, end_date.month, 1)
        first_day_of_next_end_month = first_day_of_end_month + \
                                      datetime.timedelta(days=calendar.monthrange(end_date.year, end_date.month)[1])
        date_list_query = db.session.query(distinct(func.DATE_FORMAT(Calendar.date, "%Y-%m")).label("d")). \
            filter(Calendar.date >= first_day_of_start_month). \
            filter(Calendar.date < first_day_of_next_end_month). \
            subquery()

        list_by_day = db.session.query(date_list_query.c.d, func.count(WeiboList.id).label("counts")). \
            outerjoin(WeiboList, date_list_query.c.d == func.DATE_FORMAT(WeiboList.created_at, "%Y-%m")). \
            group_by(date_list_query.c.d). \
            order_by(date_list_query.c.d).all()

        for one_record in list_by_day:
            record_list.append({
                "date": one_record[0],
                "count": one_record[1]
            })

        result = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "time_interval": time_interval,
            "record": record_list
        }
    elif time_interval == "week":
        date_list_query = db.session.query(distinct(func.DATE_FORMAT(Calendar.date, "%X年第%v周")).label("d")). \
            filter(Calendar.date >= start_date.isoformat()). \
            filter(Calendar.date < end_date.isoformat()). \
            subquery()

        list_by_day = db.session.query(date_list_query.c.d, func.count(WeiboList.id).label("counts")). \
            outerjoin(WeiboList, date_list_query.c.d == func.DATE_FORMAT(WeiboList.created_at, "%X年第%v周")). \
            group_by(date_list_query.c.d). \
            order_by(date_list_query.c.d).all()

        for one_record in list_by_day:
            record_list.append({
                "date": one_record[0],
                "count": one_record[1]
            })

        result = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "time_interval": time_interval,
            "record": record_list
        }
    elif time_interval == "year":
        date_list_query = db.session.query(distinct(Calendar.year).label("d")). \
            filter(Calendar.date >= start_date.isoformat()). \
            filter(Calendar.date <= end_date.isoformat()). \
            subquery()

        list_by_day = db.session.query(date_list_query.c.d, func.count(WeiboList.id).label("counts")). \
            outerjoin(WeiboList, date_list_query.c.d == func.YEAR(WeiboList.created_at)). \
            group_by(date_list_query.c.d). \
            order_by(date_list_query.c.d).all()

        for one_record in list_by_day:
            record_list.append({
                "date": one_record[0],
                "count": one_record[1]
            })

        result = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "time_interval": time_interval,
            "record": record_list
        }
    else:
        result = {}

    return jsonify(result)

@api_app.route('/statistic/punchcard')
@login_required
def get_statistis_punchcard():
    # process query params
    default_end_date = datetime.date.today()
    default_start_date = default_end_date - datetime.timedelta(days=30)

    start_date = request.args.get('start_date', '')
    if start_date == '':
        start_date = default_start_date
    else:
        start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_datetime.date()

    end_date = request.args.get('end_date', '')
    if end_date == '':
        end_date = default_end_date
    else:
        end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_datetime.date()

    # SELECT WEEKDAY(`c`.`date`) AS d,
    # COUNT(`l`.`id`) AS count
    # FROM (
    #  SELECT date as date
    #  FROM calendar
    #  WHERE date>='2014-01-01'
    #  AND date<='2014-03-28'
    # )AS c
    # LEFT JOIN weibo_list AS l
    # ON DATE(`l`.`created_at`) = `c`.`date` #AND FLOOR(HOUR(`l`.`created_at`)/6) = 1
    # GROUP BY d
    # ORDER BY d;
    record_list = []

    for hour_type in range(4):
        date_list_query = db.session.query(Calendar.date.label("d")). \
            filter(Calendar.date >= start_date.isoformat()). \
            filter(Calendar.date <= end_date.isoformat()). \
            subquery()

        list_by_hour_type = db.session.query(func.WEEKDAY(date_list_query.c.d).label('wd'),
                                             func.count(WeiboList.id).label("counts")). \
            outerjoin(WeiboList, and_(date_list_query.c.d == func.DATE(WeiboList.created_at),
                                      func.FLOOR(func.HOUR(WeiboList.created_at)/6) == hour_type)). \
            group_by(func.WEEKDAY(date_list_query.c.d)). \
            order_by(func.WEEKDAY(date_list_query.c.d)).all()
        for one_record in list_by_hour_type:
            record_list.append({
                "weekday": one_record[0],
                "hour_type": hour_type,
                "count": one_record[1]
            })

    record_list.sort(
        key=lambda l: (l['weekday'], l['hour_type'])
    )

    result = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "record": record_list
    }
    return jsonify(result)