from flask_restful import Resource
from flask import request, redirect, url_for
from my_server.app import api
from my_server.app import db
from my_server.model.application.hub import Hub
from my_server.model.application.user import User
from my_server.routes.oauth import current_user

@api.resource(('/hub_register'))
class hub_register(Resource):
    def get(self):
        # user = request.oauth.user
        # username = 'a'
        # user = User.query.filter_by(username=username).first()
        user = current_user()
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

@api.resource('/hub_status')
class hub_status(Resource):
    def post(self):
        print('req.args',request.args)
        print('req.base_url',request.base_url)

        print('req.data', request.get_json()['username'])
        # 안됨 print('req.username', request.get_json('username'))
        # 안됨 print('req.form', request.form['username'])

        username = request.get_json()['username']
        user = User.query.filter_by(username=username).first()
        hub = Hub.query.filter_by(user_id=user.id).first()
        print('username', username)

        if hub:
            req_body = 'Hub ok, Hub_id : '+hub.hub_id
        else:
            req_body = 'You have no Hub'
        return req_body
