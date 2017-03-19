from flask import request, render_template, session, redirect, url_for, jsonify
from my_server.form.user import SignInForm

from my_server.app import app, db
from my_server.app import oauth_provider

from my_server.model.application.user import User

from my_server.form.user import SignInForm, SignUpForm

def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None

@app.route('/')
def index():
    user = current_user()
    return render_template('index.html', user=user)

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

@app.route('/api/signout')
@oauth_provider.require_oauth()
def api_signout():
    print('api', 'signout')
    session.pop('id', None)
    if not current_user():
        print('current')
    # session.pop('remote_oauth', None)

    return 'ho'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():
        # return render_template('index.html.html', form=form)
        return redirect('http://127.0.0.1:8000')

    return render_template('signup.html', form=form)

@app.route('/signdel')
def signdel():
    return redirect(url_for('index'))