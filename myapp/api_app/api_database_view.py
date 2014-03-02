# encoding: utf-8

import datetime
from flask import request, url_for, render_template, jsonify, redirect, flash
from flask.ext.security import login_required, current_user, login_user, logout_user

from myapp import app, db
from myapp.api_app import api_app
from myapp.models import Calendar

@api_app.route("/create-database")
def create_database():
    print "begin create database"
    db.create_all()
    return "OK"

@api_app.route("/table/create/calendar")
def create_table_calendar():
    start_date = datetime.date(2009, 01, 01)
    end_date = datetime.date(2030, 12, 31)
    current_date = start_date
    d = datetime.timedelta(1)
    while current_date <= end_date:
        calendar = Calendar()
        calendar.date = current_date.strftime("%Y-%m-%d")
        calendar.year = current_date.strftime("%Y")
        calendar.month = current_date.strftime("%m")
        calendar.day = current_date.strftime("%d")
        db.session.add(calendar)
        current_date += d

    db.session.commit()
    return "Finish"