from flask import request, render_template, session, redirect, url_for, jsonify
from my_server.form.user import SignInForm
from werkzeug.security import gen_salt

from my_server.app import app, db

from my_server.model.application.user import User
from my_server.model.oauth.client import Client


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None

@app.route('/')
def index():
    user = current_user()
    return render_template('index.html', user=user)

@app.route('/add', methods=['GET', 'POST'])
def add():
    us = request.args['us']
    ps = request.args['ps']
    print(us, ps)
    item = User(username=us, ps=ps)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    user = current_user()
    if user:
        return render_template('index.html', user=user)

    form = SignInForm(request.form)
    if request.method == 'POST':
        print('post')
        username = form.username.data
        password = form.password.data

        user_by_username = User.query.filter_by(username=username).first()
        print('user', user_by_username)
        if user_by_username and user_by_username.ps == password:
            session['id'] = user_by_username.id
            print(session['id'])
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
    session.pop('id', None)
    # session.pop('remote_oauth', None)
    return redirect(url_for('index'))

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