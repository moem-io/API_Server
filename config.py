import os

SECRET_KEY = os.environ['SECRET_KEY']
DB_NAME = os.environ['DB_NAME']
DB_ID = os.environ['DB_ID']
DB_PS = os.environ['DB_PS']
DB_HOST = os.environ['DB_HOST']

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_ID,
                                                                   DB_PS,
                                                                   DB_HOST,
                                                                   DB_NAME)

REDIRECT_URI = os.environ['REDIRECT_URI']

WEB_URI = os.environ['WEB_URI']