from my_server.app import app, db
from datetime import datetime, timedelta

from flask import redirect, jsonify, request, render_template, session, url_for, flash
from my_server.model.oauth.client import Client

from my_server.model.oauth.grant import Grant
from my_server.model.oauth.token import Token
from my_server.model.application.user import User

from my_server.app import oauth_provider


from my_server.form.user import SignInForm


#---
def current_user():
    if 'id' in session:
        print('id')
        uid = session['id']
        return User.query.get(uid)
    return None


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth_provider.token_handler
def access_token():
    return None

@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth_provider.authorize_handler
def authorize(*args, **kwargs):
    print('authorize')
    form = SignInForm(request.form)
    username = form.username.data

    if request.method == 'GET':
        user = current_user()
        if not user:
            print('signin on oauth/authorize')

            # client_id = kwargs.get('client_id')
            # client = Client.query.filter_by(client_id=client_id).first()
            #
            # kwargs['client'] = client
            # kwargs['user'] = user

            # return render_template('signin_oauth2.html', form=form, **kwargs)
            return render_template('signin_oauth.html', form=form)
        else:
            return True
    elif request.method == 'POST':

        # user = current_user()
        user = User.query.filter_by(username=username).first()

        # client_id = kwargs.get('client_id')
        # client_id = request.form['client_id']
        # client = Client.query.filter_by(client_id=client_id).first()

        # kwargs['client'] = client
        # kwargs['user'] = user

        # print('kwargs', kwargs)
        # username = form.username.data
        password = form.password.data
        # print('username', username)

        # user = User.query.filter_by(username=username).first()
        # print('username', user.username)
        if user and password == user.ps:
            session['id'] = user.id

            # kwargs['user'] = user
            # print('kwargs', kwargs['user'])
            return True
    flash('아이디 비번 확인 필요', 'error')
    return redirect(url_for('index'))

@app.route('/api/me')
@oauth_provider.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)

#-------------------------------------get, set---------------------------------------#
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
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
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