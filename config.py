import os

SECRET_KEY = os.environ['SECRET_KEY']
DB_NAME = os.environ['DB_NAME']
DB_ID = os.environ['DB_ID']
DB_PS = os.environ['DB_PS']
DB_HOST = os.environ['DB_HOST']

EX_DB = os.environ['EX_DB']

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_ID,
                                                                   DB_PS,
                                                                   DB_HOST,
                                                                   DB_NAME)

SQLALCHEMY_BINDS = {
    'fl_db': "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_ID,
                                                      DB_PS,
                                                      DB_HOST,
                                                      DB_NAME),
    'hub_db': "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_ID,
                                                       DB_PS,
                                                       DB_HOST,
                                                       EX_DB),
}

# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO = 'True'

TEMPLATES_AUTO_RELOAD = True

REDIRECT_URI = os.environ['REDIRECT_URI']

WEB_URI = os.environ['WEB_URI']
