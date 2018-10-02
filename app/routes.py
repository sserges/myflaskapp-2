from flask import (
    flash,
    url_for,
    session,
    logging,
    redirect,
    request,
    render_template
)

from passlib.hash import sha256_crypt

from app import app, db
from .models import User
from .forms import RegisterForm
from .data import Articles

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data).strip())

        user = User(
            name=str(name).strip(),
            email=str(email).strip(),
            username=str(username).strip(),
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        query = User.query.filter_by(username=f'{username}')
        result = query.count()

        if result > 0:
            # Get stored hash
            data = query.first()
            password = data.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
            else:
                app.logger.info('PASSWORD NOT MATCHED')
        else:
            app.logger.info('NO USER')

    return render_template('login.html')
