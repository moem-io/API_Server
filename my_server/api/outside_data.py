from flask_restful import Resource
from flask import request
from my_server.app import api

from requests import post, get

from my_server.app import app, db

from my_server.model.application.outside_data import Weather

# from sqlalchemy.ext.serializer import loads, dumps
from flask import jsonify
from my_server.model.application.outside_data import Mise

# @api.resource('/')
# class index(Resource):
#     def get(self):
#         return 'hello api server!!'

#
@api.resource('/outside/weather')
class outside_weather(Resource):
    def get(self):
        w = Weather.query.all()
        # print(w)
        # for i in w:
        #     print(i.serialize)

        # print('hoho'+str(jsonify(json_list=[i.serialize for i in w])))
        return jsonify(json_list=[i.serialize for i in w])

    # def post(self):
    #     req_body = request.get_json()
    #     req_body = request.form['title']
        # print(req_body)
        # return req_body

@api.resource('/outside/mise')
class outside_mise(Resource):
    def get(self):
        w = Mise.query.all()
        return jsonify(json_list=[i.serialize for i in w])

