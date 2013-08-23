from flask import Flask
import os

app = Flask(__name__)
#open debug model
if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    app.config['ONLINE']=True
    pass
else:
    # Local
    app.config['ONLINE']=False
    app.debug = True

# import view
from myapp import views