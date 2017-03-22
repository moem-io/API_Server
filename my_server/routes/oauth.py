from my_server.app import app, db
from datetime import datetime, timedelta

from werkzeug.security import gen_salt

from flask import redirect, jsonify, request, render_template, session, url_for, flash
from my_server.model.oauth.client import Client

from my_server.model.oauth.grant import Grant
from my_server.model.oauth.token import Token
from my_server.model.application.user import User

from my_server.app import oauth_provider


from my_server.form.user import SignInForm

import bcrypt

#---
# def current_user():
#     if 'id' in session:
#         print('id')
#         uid = session['id']
#         return User.query.get(uid)
#     return None

@app.route('/api/me')
@oauth_provider.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)

@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth_provider.authorize_handler
def authorize(*args, **kwargs):
    print('authorize')
    form = SignInForm(request.form)
    if request.method == 'GET':
        return render_template('signin_form.html', form=form)
    elif request.method == 'POST':
        print('post')
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        password = form.password.data

        if user and user.is_valid_password(password):
            print('hashed', 'ok')
            return True

        flash('아이디, 비밀번호 확인 필요', 'error')
    return render_template('signin_form.html', form=form)


#-------------------------------------get, set---------------------------------------#

@app.route('/client')
def client():
    user = current_user()
    if not user:
        return redirect('/')
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
            ]),
        _default_scopes='email',
        user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )


@oauth_provider.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth_provider.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth_provider.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)

    username = request.body.get('username')
    user = User.query.filter_by(username=username).first()

    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=user,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant



@oauth_provider.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth_provider.tokensetter
def save_token(token, request, *args, **kwargs):
    # print('savetoken', kwargs['user'])
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok

@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth_provider.token_handler
def access_token():
    return None