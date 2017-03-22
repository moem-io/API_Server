from flask import request, render_template, session, redirect, url_for, jsonify
from my_server.form.user import SignInForm
from werkzeug.security import gen_salt

from my_server.app import app, db

from my_server.model.application.user import User
# from my_server.routes.oauth import current_user
from my_server.form.user import SignInForm, SignUpForm

from my_server.model.oauth.client import Client
import os


@app.route('/test/add/user', methods=['GET', 'POST'])
def add_user():
    us = request.args['us']
    ps = request.args['ps']
    print(us, ps)
    item = User(username=us, ps=ps)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))


# @app.route('/test/add/client', methods=['GET', 'POST'])
# def add_client():
#     user = current_user()
#     if not user:
#         return redirect('/')
#     re = app.config.get('REDIRECT_URI')
#     item = Client(
#         client_id=gen_salt(40),
#         client_secret=gen_salt(50),
#         _redirect_uris=' '.join([
#             re,
#         ]),
#         _default_scopes='email',
#         user_id=user.id,
#     )
#     db.session.add(item)
#     db.session.commit()
#     return jsonify(
#         client_id=item.client_id,
#         client_secret=item.client_secret,
#     )
