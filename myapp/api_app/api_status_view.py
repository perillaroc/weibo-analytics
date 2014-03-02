# encoding: utf-8
import json
import datetime
import string

from flask import request, g, jsonify

from flask.ext.security import login_required

from myapp.models import WeiboList
from myapp import app, db

from weibo import APIClient

client = APIClient(app_key=app.config['APP_KEY'],
                   app_secret=app.config['APP_SECRET'],
                   redirect_uri=app.config['CALLBACK_URL'])

@app.route('/status/total-number')
@login_required
def get_status_total_number():
    token = json.loads(g.user.token)
    client.set_access_token(token['access_token'], token['expires'])
    statuses = client.statuses.user_timeline.get(count=10, page=1)
    results = {'total_number': statuses['total_number']}
    error_results = {'request':'/status/total-number',
                     'error_code':-1,
                     'error':'error'}
    return jsonify(results)

@app.route('/status/update')
@login_required
def update_status():
    page_no = int(request.args.get('page', '1'))
    if page_no < 1:
        page_no = 1
    count_per_page = int(request.args.get('count', '80'))
    if count_per_page > 100:
        count_per_page = 100

    user = g.user
    print user.token
    token_1 = g.user.token
    token = json.loads(token_1)
    client.set_access_token(token['access_token'], token['expires'])
    weibo_results = client.statuses.user_timeline.get(count=count_per_page, page=page_no)
    statuses = weibo_results['statuses']
    for status in statuses:
        current_status = WeiboList.query.filter_by(uid=status['id']).first()
        if current_status is None:
            #print "Creating status"
            current_status = WeiboList()
            current_status.uid = status['id']
            current_status.user_uid = status['user']['id']
            current_status.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_status.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_status.status_type = -1

            current_status.status_id = status['id']

            created_at = datetime.datetime.strptime(string.replace(status['created_at'], "+0800 ", ""),
                                                    '%a %b %d %H:%M:%S %Y')
            current_status.created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
            current_status.source = status['source'].encode("utf-8")

            current_status.original_pic = status.get('original_pic', '')
            current_status.bmiddle_pic = status.get('bmiddle_pic', '')
            current_status.thumbnail_pic = status.get('thumbnail_pic', '')

            current_status.geo = json.dumps(status['geo'])

            current_status.retweeted_status = json.dumps(status.get('retweeted_status', ''),
                                                         ensure_ascii=False)

            current_status.reposts_count = status['reposts_count']
            current_status.comments_count = status['comments_count']
            current_status.attitudes_count = status['attitudes_count']
            current_status.visible_type = status['visible'].type

            current_status.pic_urls = json.dumps(status['pic_urls'])

            db.session.add(current_status)
        else:
            #print "Status has been created"
            current_status.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_status.status_type = -1

            current_status.original_pic = status.get('original_pic', '')
            current_status.bmiddle_pic = status.get('bmiddle_pic', '')
            current_status.thumbnail_pic = status.get('thumbnail_pic', '')

            current_status.geo = json.dumps(status['geo'])

            current_status.retweeted_status = json.dumps(status.get('retweeted_status', ''),
                                                         ensure_ascii=False)

            current_status.reposts_count = status['reposts_count']
            current_status.comments_count = status['comments_count']
            current_status.attitudes_count = status['attitudes_count']
            current_status.visible_type = status['visible'].type

            current_status.pic_urls = json.dumps(status['pic_urls'])

    db.session.commit()

    results = {"count": count_per_page,
               "page": page_no,
               "max_id": statuses[0]['id'],
               "since_id": statuses[len(statuses)-1]['id'],
               'total_num': weibo_results['total_number']}
    return jsonify(results)
