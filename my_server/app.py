from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
from flask_bcrypt import Bcrypt

app = Flask(__name__)
api = Api(app)

bcrypt = Bcrypt(app)

app.config.from_object('config')
# app.secret_key = 'secret'

db = SQLAlchemy(app)

oauth_provider = OAuth2Provider(app)


from my_server.model import *

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/fl_db'
# app.config.update({
#     'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:1234@localhost/fl_db',
# })
# for x in ['DB_NAME', 'DB_NAME2']:
#     db.create_all(bind=app.config[x])
db.create_all(bind=app.config['DB_NAME'])
db.create_all(bind=app.config['EX_DB'])

from my_server.api import *
from my_server.routes import *
