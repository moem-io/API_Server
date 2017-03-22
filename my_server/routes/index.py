from flask import request, render_template, session, redirect, url_for, jsonify, flash
from my_server.form.user import SignInForm

from my_server.app import app, db
from my_server.app import oauth_provider

from my_server.model.application.user import User

from my_server.form.user import SignInForm, SignUpForm

from my_server.app import bcrypt

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():
        # return render_template('index.html.html', form=form)
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        password = form.password.data
        password_check = form.password_check.data

        if user:
            flash('아이디가 이미 존재합니다.', 'error')
            print('id')
            return render_template('signup.html', form=form)
        elif password == password_check:
            hashed = bcrypt.generate_password_hash(password)

            name = form.name.data
            belong = form.belong.data

            print('hashed', hashed)
            item = User(username=username, ps=hashed, name=name, belong=belong)
            db.session.add(item)
            db.session.commit()
            print('ok')

            return redirect(app.config['WEB_URI'])
        else:
            print('diff')

            flash('비밀번호가 다릅니다.', 'error')

    return render_template('signup.html', form=form)


@app.route('/signdel')
def signdel():
    return redirect(url_for('index'))
