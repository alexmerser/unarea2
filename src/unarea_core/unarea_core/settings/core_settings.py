class DefaultSettings(object):
    DEBUG = True

class Local(object):
    DEBUG = True
    MONGODB_SETTINGS = {'host': 'localhost', 'db': 'unarea2'}
    SECRET_KEY = 'secret$111!!!'
    SECURITY_PASSWORD_HASH = 'bcrypt'
