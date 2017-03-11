from flask_restful import Resource
from flask import request
from my_server.app import api

# @api.resource('/')
# class index(Resource):
#     def get(self):
#         return 'hello api server!!'

@api.resource('/board')
class board(Resource):
    def post(self):
        req_body = request.get_json()
        # req_body = request.form['title']
        print(req_body)
        return req_body

