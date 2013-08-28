import os

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