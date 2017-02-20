from flask import request, render_template, session, redirect, url_for, jsonify
from my_server.form.user import SignInForm

from my_server.app import app, db

from my_server.model.application.user import User

from my_server.form.user import SignInForm, SignUpForm


@app.route('test/add', methods=['GET', 'POST'])
def add():
    us = request.args['us']
    ps = request.args['ps']
    print(us, ps)
    item = User(username=us, ps=ps)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))
