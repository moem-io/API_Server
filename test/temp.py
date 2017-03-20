# auto login for future

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