# encoding: utf-8
from flask import Flask, request, url_for, render_template, g, redirect
from flask.ext.security import login_required, current_user
from myapp import app
from myapp.thirdparty import flickr as flickr
if app.config['ONLINE']:
    import pylibmc
else:
    import sae.memcache as pylibmc

from weibo import APIClient
import json

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

    client = APIClient(app_key=app.config['APP_KEY'], \
        app_secret=app.config['APP_SECRET'], redirect_uri=app.config['CALLBACK_URL'])
    authorize_url = client.get_authorize_url()
    #print authorize_url

    return render_template('welcome.html', front_image_list=front_image_list, authorize_url=authorize_url)

@app.route('/logout')
@login_required
def logout():
    return redirect('/api/user/logout')

@app.route('/')
@app.route('/index')
@login_required
def index():
    print g.user.info
    g.user.info = json.loads(g.user.info)
    return render_template('index.html', user=g.user)


from myapp.api_app import api_app
app.register_blueprint(api_app,url_prefix='/api')