from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from my_server.app import api
from my_server.app import db
from my_server.model.application.hub import Hub
from my_server.model.application.user import User
# from my_server.routes.oauth import current_user
from my_server.app import oauth_provider, app
import paho.mqtt.client as mqtt


@app.route('/api/hub_register', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def hub_register():
    user = request.oauth.user
    if user:
        print('username', user.username)

        hub = Hub.query.filter_by(user_id=user.id).first()
        if not hub:
            print('make hub')
            hub_id = 'abcdefg'
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
def upload():
    user = request.oauth.user
    upload_app = request.form['upload_app']
    print('upload_app', upload_app)

    return jsonify(username=user.username)


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
    mqttc.publish("hello/world", "123")  # 'hello/world' 토픽에 "Hello World!"라는 메시지 발행
    mqttc.loop(2)
    return 'suc'