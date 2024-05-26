from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Libraries


@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route('/resources')
def resources():
    dictionary: dict = dict()
    data = db.session.scalars(sa.select(Libraries)).all()
    for d in data:
        lang = d.language
        framework = d.framework
        desc = d.description
        review = d.review
        docs = d.docs
        example = d.example

        if lang not in dictionary:
            dictionary[lang] = {}

        dictionary[lang][framework] = [desc, review, docs, example]
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('resources.html', data=dictionary)


@app.route('/support')
def support():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('support.html')


@app.route('/skills')
def skills():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    team_members = [
        {
            'username': 'Максим Журавлев',
            'image': 'profile1.webp',
            'skills': 'Python, C++',
            'libraries': 'Django, Fast API',
            'role': 'Backend',
            'number': 1
        },
        {
            'username': 'Владислав Голосной',
            'image': 'profile2.webp',
            'skills': 'Python',
            'libraries': '-',
            'role': 'Designer',
            'number': 2
        },
    ]
    return render_template('skills.html', team_members=team_members)


@app.route('/network')
def network():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('network.html')


@app.route('/webinars')
def webinars():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('webinars.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
