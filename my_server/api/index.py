from flask_restful import Resource
from flask import request
from sqlalchemy.ext.declarative import DeclarativeMeta

from my_server.app import api
from my_server.model.application.hub import Hub
from flask import jsonify
from my_server.model.application.app_model import AppModel
from my_server.model.application.app_setting import AppSetting
from my_server.model.application.outside_data import *
from my_server.app import db
import json


# @api.resource('/')
# class index(Resource):
#     def get(self):
#         return 'hello api server!!'

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)



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

@api.resource('/app_info')
class app_info(Resource):
    def get(self):
        app_model = AppModel.query.all()
        app_model_json = json.dumps(app_model, cls=AlchemyEncoder)
        # print('data', app_model_json)
        # print('data type', type(app_model_json))

        data = {}
        data['apps'] = [{'app_num': 1,
                         'app_name': '기상청 온도로 창문 닫기',
                         'app_detail': '기상청의 온도를 가져와 창문을 닫아보자!',
                         'app_switch': True,
                         'app_input': '기상청 온도 및 습도',
                         'app_input_detail': [{'icon': 'sun icon', 'value': '24°C'}, {'icon': 'theme icon', 'value': '14%'}],
                         'app_output': '서보 모터',
                         'app_output_detail': True,
                         },
                        {'app_num': 2,
                         'app_name': '두번째앱2',
                         'app_detail': 'ㅎㅎ',
                         'app_switch': False,
                         'app_input': 'ㄸ',
                         'app_input_detail': [{'icon': 'hand rock icon', 'value': '두 번'}, {'icon': 'bullseye icon', 'value': '세기 : 45%'}],
                         'app_output': '서보 모터',
                         'app_output_detail': False,
                         }]

        data['apps'] = json.loads(app_model_json)
        # print('jsonify type', jsonify(data))
        return jsonify(data)

@api.resource('/n_s_info')
class n_s_info(Resource):
    def get(self):
        app_setting = AppSetting.query.all()
        app_setting_json = json.dumps(app_setting, cls=AlchemyEncoder)
        # print('data', app_model_json)
        # print('data type', type(app_model_json))
        data = {}
        data['n_s'] = json.loads(app_setting_json)
        # print('jsonify type', jsonify(data))
        return jsonify(data)


@api.resource('/ex_info')
class ex_info(Resource):
    def get(self):
        mise = Mise.query.all()[0]
        weather = Weather.query.all()
        mise_json = json.dumps(mise, cls=AlchemyEncoder)
        weather_json = json.dumps(weather, cls=AlchemyEncoder)

        data = {}
        data['mise'] = json.loads(mise_json)
        data['weather'] = json.loads(weather_json)
        # print('jsonify type', data['mise'])


        return jsonify(data)