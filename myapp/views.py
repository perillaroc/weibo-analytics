# encoding: utf-8
from flask import request, url_for, render_template, g, redirect
from flask.ext.security import login_required, current_user
from myapp import app, db

from myapp.models import WeiboList
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct, and_, union_all

if app.config['ONLINE']:
    import pylibmc
else:
    import sae.memcache as pylibmc

from weibo import APIClient
import json

client = APIClient(app_key = app.config['APP_KEY'],
                       app_secret = app.config['APP_SECRET'],
                       redirect_uri = app.config['CALLBACK_URL'])

@app.before_request
def before_request():
    g.user = current_user


@app.route('/login')
def login():
    import random
    # fetch for
    mc = pylibmc.Client()
    front_image_list = mc.get("front_image_list")
    if not front_image_list:
        front_image = {}
        # photos = flickr.interestingness()
        # photo_no = random.randint(0, len(photos) - 1)
        # photos_sizes = photos[photo_no].getSizes()
        # front_image['index'] = photo_no
        # front_image['url'] = photos_sizes[0]['source']
        # for a_size in photos_sizes:
        #     if a_size['label'] == 'Medium 640':
        #         front_image['source'] = a_size['source']
        #         front_image['url'] = a_size['url']
        # front_image_list = []
        # front_image_list.append(front_image)
    else:
        random.shuffle(front_image_list)


    authorize_url = client.get_authorize_url()
    # print authorize_url

    return render_template('welcome.html',
                           front_image_list = front_image_list,
                           authorize_url = authorize_url)

@app.route('/logout')
@login_required
def logout():
    return redirect('/api/user/logout')


@app.route('/')
@app.route('/index')
@login_required
def index():
    g.user.info = json.loads(g.user.info)
    return render_template('index.html', user=g.user, current_navi="index")


@app.route('/update')
@login_required
def update():
    g.user.info = json.loads(g.user.info)

    #get oldest and lateset status in database
    query_latest = db.session.query(WeiboList).filter(WeiboList.user_uid == g.user.uid)\
        .order_by(WeiboList.created_at.desc()).limit(1).subquery().select()
    query_oldest = db.session.query(WeiboList).filter(WeiboList.user_uid == g.user.uid)\
        .order_by(WeiboList.created_at).limit(1).subquery().select()
    query = db.session.query(WeiboList).select_from(union_all(query_latest,query_oldest)).order_by(WeiboList.created_at)
    records = query.all()
    oldest_datetime = records[0].created_at
    latest_datetime = records[1].created_at
    latest_uid = records[1].uid

    # get total count in database
    total_count_in_database = db.session.query(func.count(WeiboList)) \
        .filter(WeiboList.user_uid == g.user.uid).first()[0]

    # get total count of update status
    token = json.loads(g.user.token)
    client.set_access_token(token['access_token'], token['expires'])
    statuses = client.statuses.user_timeline.get(count=10, page=1, since_id=latest_uid)
    total_count = statuses['total_number']

    page_info = {
        "oldest_date": oldest_datetime.date().isoformat(),
        "latest_date": latest_datetime.date().isoformat(),
        "total_count_in_database": total_count_in_database,
        "total_count_for_update": total_count - total_count_in_database
    }

    return render_template('update.html', user=g.user, current_navi="update", page_info=page_info)

@app.route('/statistic')
@login_required
def statistic():
    g.user.info = json.loads(g.user.info)
    return render_template('statistic/overview.html', user=g.user, current_navi="statistic")

@app.route('/statistic/punchcard')
@login_required
def statistic_punchcard():
    g.user.info = json.loads(g.user.info)
    return render_template('statistic/punchcard.html', user=g.user, current_navi="statistic")

@app.route('/statistic/type')
@login_required
def statistic_type():
    g.user.info = json.loads(g.user.info)
    return render_template('statistic/type.html', user=g.user, current_navi="statistic")

@app.route('/about')
@login_required
def about():
    g.user.info = json.loads(g.user.info)
    return render_template('about.html', user=g.user, current_navi='about')


