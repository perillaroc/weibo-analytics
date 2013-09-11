# encoding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
import os

app = Flask(__name__)
app.config.from_object('myapp.fileconfig')
app.secret_key = 'A0Zrdgj/3yX R~XHH!jmN]LWX/,?RT'


db = SQLAlchemy(app)

# open debug model
if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    app.config['ONLINE'] = True
    pass
else:
    # Local
    app.config['ONLINE'] = False
    app.debug = True

# import view
from myapp import views, api_views, models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

# from weibo import APIClient

# client = APIClient(app_key=app.config['APP_KEY'], \
#         app_secret=app.config['APP_SECRET'], redirect_uri=app.config['CALLBACK_URL'])
