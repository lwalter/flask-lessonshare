from datetime import timedelta
import os


class Config(object):
    DEBUG = False

    ASSETS_DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SECRET_KEY = os.environ['SECRET_KEY']

    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = timedelta(seconds=1200)
    JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)

    JS_PATH = 'js/{0}'
    CONTROLLERS_PATH = JS_PATH.format('controllers/{0}')
    SERVICES_PATH = JS_PATH.format('services/{0}')
    JS_LIB_PATH = 'libs/{0}'
    CSS_PATH = 'css/{0}'
    CSS_LIB_PATH = JS_LIB_PATH.format('angular-material/{0}')


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = True


class Production(Config):
    PRODUCTION = True
