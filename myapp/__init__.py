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
    app.debug = True
else:
    # Local
    app.config['ONLINE'] = False
    app.debug = True

# import views
from myapp import views, test_views

# import blueprint
from myapp.api_app import api_app
app.register_blueprint(api_app, url_prefix = '/api')


# import models
from myapp import models
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


