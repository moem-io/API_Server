from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
api = Api(app)

app.config.from_object('config')
# app.secret_key = 'secret'

db = SQLAlchemy(app)

oauth_provider = OAuth2Provider(app)


from my_server.model import *

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/fl_db'
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:1234@localhost/fl_db',
})
db.create_all()

from my_server.api import *
from my_server.routes import *
