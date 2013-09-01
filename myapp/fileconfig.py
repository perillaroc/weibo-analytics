import os
import sae.const

CSRF_ENABLED = True

# open debug model
if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    ONLINE = True
    pass
else:
    # Local
    ONLINE = False
    debug = True

SQLALCHEMY_DATABASE_URI="mysql+mysqldb://"+sae.const.MYSQL_USER+":"+sae.const.MYSQL_PASS+"@"+sae.const.MYSQL_HOST+":"+sae.const.MYSQL_PORT+"/"+sae.const.MYSQL_DB 

#sina weibo app

APP_KEY = '130967181'
APP_SECRET = '7ecd6b730bfeee87ae5a4f701deeaae4'
CALLBACK_URL =  'http://127.0.0.1:5000/api/user/auth-callback'