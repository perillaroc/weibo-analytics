from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('myapp.fileconfig')

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
