# encoding: utf-8
from flask import request, url_for, render_template, jsonify, redirect, flash
from flask.ext.security import login_required, current_user, login_user, logout_user
import json

from myapp.models import User
from myapp import app, db
from myapp.api_app import api_app

if app.config['ONLINE']:
    import pylibmc
else:
    import sae.memcache as pylibmc

from weibo import APIClient
client = APIClient(app_key = app.config['APP_KEY'],
                   app_secret = app.config['APP_SECRET'],
                   redirect_uri = app.config['CALLBACK_URL'])

@api_app.route('/update-front-image')
def update_front_image():
    '''
    update foreground image array in memcache from flickr
    '''

    import random
    from myapp.thirdparty import flickr as flickr

    total_image_count = 10
    front_image_list = []
    photos = flickr.interestingness()
    photos_select_no_list = random.sample(
        range(0, len(photos) - 1), total_image_count)
    for a_photo_no in photos_select_no_list:
        a_front_image = {}
        a_front_image['index'] = a_photo_no
        a_front_image['title'] = photos[a_photo_no].title
        a_front_image['description'] = photos[a_photo_no].description
        # size
        a_photo_sizes = photos[a_photo_no].getSizes()
        a_front_image['url'] = a_photo_sizes[0]['source']
        for a_size in a_photo_sizes:
            if a_size['label'] == 'Medium 640':
                a_front_image['source'] = a_size['source']
                a_front_image['url'] = a_size['url']
        print a_photo_no
        front_image_list.append(a_front_image)
    print front_image_list

    # store in memcache
    mc = pylibmc.Client()
    mc.set("front_image_list", front_image_list)
    front_image_list_2 = mc.get("front_image_list")
    return jsonify(front_image_list = front_image_list_2)

@api_app.route("/create-database")
def create_database():
    print "begin create database"
    db.create_all()
    return "OK"

def load_or_creator_user(token):
    '''根据token载入或创建用户
    '''
    import datetime
    user = User.query.filter_by(uid = int(token.uid)).first()
    if user is None:
        print 'user is not created'
        # create user
        user_info = client.users.show.get(uid = token.uid)
        user = User(token.uid, json.dumps(user_info), json.dumps(token))
        user.active = True
        user.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user.last_login_time = user.create_time
        db.session.add(user)
        db.session.commit()
        login_user(user)
    else:
        print 'user has been created'
        # load user
        user.token = json.dumps(token)
        user_info = client.users.show.get(uid = token.uid)
        user.info = json.dumps(user_info)
        user.active = True
        user.last_login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        login_user(user)


@api_app.route('/user/auth-callback')
def auth_call_back():
    '''
    检查用户是否存在，不存在则创建，并载入用户
    还需要错误检查
    '''
    authorization_code = request.args.get('code', '')
    token = client.request_access_token(authorization_code)
    access_token = token.access_token  # 新浪返回的token，类似abc123xyz456
    expires_in = token.expires_in  # token过期的UNIX时间
    uid = token.uid  # 用户的uid
    client.set_access_token(access_token, expires_in)
    print token
    load_or_creator_user(token)
    print current_user
    flash("Login form sina weibo")
    return redirect("/")

@api_app.route('/user/logout')
@login_required
def user_logout():
    logout_user()
    flash("you are login out!")
    return redirect('/')
