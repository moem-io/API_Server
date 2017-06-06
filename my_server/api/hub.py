from flask_restful import Resource
from flask import request, redirect, url_for, jsonify, make_response
from my_server.app import api
from my_server.app import db
from my_server.model.application.hub import Hub, node, link
from my_server.model.application.user import User
from my_server.model.application.app_model import AppModel

# from my_server.routes.oauth import current_user
from my_server.app import oauth_provider, app
import paho.mqtt.client as mqtt
import json
from my_server.api.index import AlchemyEncoder

@app.route('/api/hub_register', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def hub_register():
    user = request.oauth.user
    if user:
        print('username', user.username)

        hub = Hub.query.filter_by(user_id=user.id).first()
        if not hub:
            print('make hub')
            hub_id = '00001214'
            hub_secret = 'abcdefg'
            item = Hub(
                hub_id=hub_id,
                hub_secret=hub_secret,
                user_id=user.id,
            )
            db.session.add(item)
            db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/hub_info', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def hub_info():
    # print('req.args',request.args)
    # print('req.base_url',request.base_url)

    # print('req.data', request.get_json()['username'])
    # 안됨 print('req.username', request.get_json('username'))
    # 안됨 print('req.form', request.form['username'])

    user = request.oauth.user

    username = user.username
    user = User.query.filter_by(username=username).first()
    hub = Hub.query.filter_by(user_id=user.id).first()
    print('username', username)

    hub_alive = True

    if hub and hub_alive:
        payload = {'hub_status': '켜짐'}
        payload['hub_id'] = hub.hub_id
    elif hub:
        payload = {'hub_status': '꺼짐'}
        payload['hub_id'] = hub.hub_id
    else:
        payload = {'hub_status': '없음'}
        payload['hub_id'] = '없음'
    return jsonify(payload)


@app.route('/api/upload', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def api_upload():
    user = request.oauth.user
    upload_app = request.form['upload_app']
    print('upload_app', upload_app)

    return jsonify(username=user.username)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    upload_app_title = request.form['upload_app_title']
    upload_app_sub = request.form['upload_app_sub']
    upload_app = request.form['upload_app']
    # print('upload_app', upload_app)

    mqttc = mqtt.Client("python_pub")  # MQTT Client 오브젝트 생성
    mqttc.connect("13.124.19.161", 1883)  # MQTT 서버에 연결
    mqttc.publish("app/upload/00001214",
                  upload_app_title + ',' + upload_app_sub + ',' + upload_app)  # 'hello/world' 토픽에 "Hello World!"라는 메시지 발행
    mqttc.loop(2)

    return jsonify(username='hi')


@app.route('/switch/<int:id>', methods=['GET', 'POST'])
def switch(id):
    return jsonify(username='hi')


# @app.route('/apps/save', methods=['GET', 'POST'])
# def app_save():
#     if request.method == 'POST':
#         print('post')
#         data = request.form['data']
#         print('data', data)
#     return jsonify(username='hi')


@api.resource('/app/save')
class app_save(Resource):
    def get(self):
        return 'ho'

    def post(self):
        # req_body = request.get_json()
        # req_body = request.form['title']
        data = request.data
        print('data', json.loads(data.decode()))
        for i in json.loads(data.decode()):
            print('i', i['app_name'])

        db.session.query(AppModel).delete()

        for i in json.loads(data.decode()):
            # print('i', type(i))
            # print('i.id', type(i['id']))
            app_model = AppModel(
                id=i['id'],
                app_name=i['app_name'],
                app_detail=i['app_detail'],
                app_switch=i['app_switch'],
                app_input=i['app_input'],
                app_input_detail=i['app_input_detail'],
                app_output=i['app_output'],
                app_output_detail=i['app_output_detail'],
            )
            db.session.add(app_model)
            db.session.commit()

        return jsonify(data.decode())


@api.resource('/node/connect')
class node_connect(Resource):
    def get(self):
        if True:
            resp = make_response(200)
            return resp

        return 'go to post'

    def post(self):
        if True:
            data = request.data
            # print('data', json.loads(data.decode()))
            data_json = json.loads(data.decode())

            db.session.query(node).delete()
            db.session.query(link).delete()

            for i in data_json['node']:
                # print('i', i)
                db.session.add(node(i['name'], i['radius'], i['rgb']))
            for i in data_json['link']:
                # print('i', i)
                db.session.add(link(i['source'], i['target'], i['length']))
            db.session.commit()

            # resp = make_response(200)
            return 'success'

@api.resource('/node/connect/info')
class node_connect_info(Resource):
    def get(self):
        data = {}
        data['node'] = json.dumps(db.session.query(node).all(), cls=AlchemyEncoder)
        data['link'] = json.dumps(db.session.query(link).all(), cls=AlchemyEncoder)
        # print('data', data)
        return jsonify(data)



# test
@app.route('/api/post_test', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def post_test():
    test = request.form['abc']
    print('test', test)
    return jsonify(test=test)


@app.route('/test/mqtt', methods=['GET', 'POST'])
def test_mqtt():
    mqttc = mqtt.Client("python_pub")  # MQTT Client 오브젝트 생성
    # mqttc.connect("test.mosquitto.org", 1883)    # MQTT 서버에 연결
    mqttc.connect("13.124.19.161", 1883)  # MQTT 서버에 연결
    mqttc.publish("control/motor/00001214", "1,0")  # 'hello/world' 토픽에 "Hello World!"라는 메시지 발행
    mqttc.loop(2)
    return 'suc'
