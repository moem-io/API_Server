from flask_restful import Resource
from flask import request
from my_server.app import api
from my_server.model.application.hub import Hub

# @api.resource('/')
# class index(Resource):
#     def get(self):
#         return 'hello api server!!'

@api.resource('/board')
class board(Resource):
    def get(self):
        hub = Hub.query.filter_by(user_id=1).first()
        print(hub.id)
        return hub.id

    def post(self):
        req_body = request.get_json()
        # req_body = request.form['title']
        print(req_body)
        return req_body

