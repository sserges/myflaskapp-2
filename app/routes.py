from functools import wraps

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
from .models import User, Article
from .forms import RegisterForm, ArticleForm
from .data import Articles

# Articles = Articles()

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)


@app.route('/article/<string:id>/')
def article(id):
    article = Article.query.filter_by(id=id).first_or_404()
    return render_template('article.html', article=article)


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
        username = str(request.form['username']).strip()
        password_candidate = str(request.form['password']).strip()

        query = User.query.filter_by(username=f'{username}')
        result = query.count()

        if result > 0:
            # Get stored hash
            data = query.first()
            password = data.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid login', 'danger')
                return render_template('login.html')
        else:
            flash('Username not found', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    articles = Article.query.all()
    return render_template('dashboard.html', articles=articles)


@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    page_title = 'Add Article'
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = str(form.title.data).strip()
        body = str(form.body.data).strip()

        article = Article(title=title, body=body, author=session['username'])

        db.session.add(article)
        db.session.commit()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form, page_title=page_title)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    page_title = 'Edit Article'
    article = Article.query.filter_by(id=id).first_or_404()
    form = ArticleForm(request.form)

    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        title = str(request.form['title']).strip()
        body = str(request.form['body']).strip()

        article.title = title
        article.body = body

        db.session.commit()
        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form, page_title=page_title)


@app.route('/delete_article/<string:id>')
@is_logged_in
def delete_article(id):
    article = Article.query.filter_by(id=id).first_or_404()
    db.session.delete(article)
    db.session.commit()
    flash('Article Deleted', 'success')
    return redirect('dashboard')