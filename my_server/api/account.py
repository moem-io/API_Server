from flask_restful import Resource

from my_server.app import api
from my_server.app import db
from my_server.model.application.user import User

#
# # TODO 해커가 막 쏘면 어떻게 막아야 하지?
# @api.resource('/signup')
# class signup(Resource):
#     def get(self):
#
#         us = User('nick3', 'hi')
#
#
#         db.session.add(us)
#         db.session.commit()
#
#         print(User.query.all())
#
#         # return User.query.all() # 안 됨 JSON으로 안된다네
