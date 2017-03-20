from flask import request, render_template, session, redirect, url_for, jsonify
from my_server.form.user import SignInForm

from my_server.app import app, db
from my_server.app import oauth_provider

from my_server.model.application.user import User

from my_server.form.user import SignInForm, SignUpForm


@app.route('/')
def index():
    return render_template('index.html')

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