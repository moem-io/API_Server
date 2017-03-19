from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from my_server.app import api
from my_server.app import db
from my_server.model.application.hub import Hub
from my_server.model.application.user import User
from my_server.routes.oauth import current_user
from my_server.app import oauth_provider, app


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

    if hub:
        payload = {'hub_status': 'OK'}
        payload['hub_id'] = hub.hub_id
    else:
        payload = {'hub_status': 'XX'}
        payload['hub_id'] = 'XX'
    return jsonify(payload)


@app.route('/api/post_test', methods=['GET', 'POST'])
@oauth_provider.require_oauth()
def post_test():
    test = request.form['abc']
    print('test', test)
    return jsonify(test=test)
