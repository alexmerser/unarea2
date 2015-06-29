import os

 
# root
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
 
 
# port
DEBUG = True
PORT = 8000
SSL = False
CDN = False
CDN_PREFIX = None
PREFORK_PROCESS = 0
XSRF_COOKIE = False
COOKIE_SECRET = "ASG@#sdlh0o(@#*YI(SDF08yrt1(*YIOUSAHF"
COOKIE_USER_SESSION = u'user_session'
LOGIN_URL = u'/auth/login'
 
 
# handlers
# HANDLERS_PKG = u'module.handlers'
# HANDLERS_LIST = (u'module_name', u'module_name')
 
 
# session
SESSION = dict(
    engine=u'memcached',
    servers=(u'127.0.0.1:11211',),
    serializer=u'marshal',
    username=u'memsupport',
    password=u'',
)
 
 
# database (default)
DATABASE_NAME = u'database_name'
DATABASE_RSET = u'r0'
DATABASE_HURI = u'127.0.0.1:27000,' \
                u'127.0.0.1:27001,' \
                u'127.0.0.1:27002,' \
                u'127.0.0.1:27003'
DATABASE_HOST = u'127.0.0.1'
DATABASE_PORT = 27000
DATABASE_CONN = 100
DATABASE_AREQ = True
DATABASE_UGLS = True
DATABASE_USER = None
DATABASE_PASS = None
 
 
# database (track, notify)
DATABASE_TRACK_NAME = u'database_tracking'
DATABASE_NOTIFY_NAME = u'database_notifications'
 
 
# graph (social)
GRAPH_SOCIAL_NAME = u'social'
GRAPH_SOCIAL_HOST = u'127.0.0.1'
GRAPH_SOCIAL_PORT = 8529
GRAPH_SOCIAL_USER = u'graphsupport'
GRAPH_SOCIAL_PASS = u''
 
 
# queues
RABBITMQ_TRACK_NAME = u'tracking'
RABBITMQ_TRACK_BROK = u'amqp://guest:guest@127.0.0.1//'
 
 
# email
EMAIL_ACCOUNT = u''
EMAIL_USER = u''
EMAIL_PASS = u''
EMAIL_HOST = u'smtp.google.com'
EMAIL_PORT = 587
EMAIL_TLS = True
 
 
# site
SITE_TITLE = u''
SITE_DESCRIPTION = u''
SITE_DOMAIN = u'127.0.0.1'
SITE_ROOT = u'/'
SITE_STATIC = SITE_ROOT + u'static'
 
 
# paths
CA_PATH = os.path.join(ROOT_PATH, u'CA')
STATIC_PATH = os.path.join(ROOT_PATH, u'static')
TEMPLATES_PATH = os.path.join(ROOT_PATH, u'templates')
TEMP_PATH = u'/tmp'
 
 
# autoreload
AUTORELOAD_ENABLED = True
AUTORELOAD_FILES = ()
 
 
# static files
STATIC_FILES = ()