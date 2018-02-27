from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from app import app
from app import db
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'rong'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'I am hungary!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Hello', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	# 已经登陆的用户自动回到主页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # 验证用户名和密码
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # 登陆名无效 或者 密码错误
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # flask-login 插件里的函数: login_user()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

