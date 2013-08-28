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