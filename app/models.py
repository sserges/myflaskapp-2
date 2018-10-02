from app import db

class User(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(100), index=True)
    email           = db.Column(db.String(100), index=True, unique=True)
    username        = db.Column(db.String(30), index=True, unique=True)
    password        = db.Column(db.String(100))
    register_date   = db.Column(db.DateTime, default=db.func.now())

    def __str__(self):
        return f"<User {self.username}>"

    def __repr__(self):
        return f"<User {self.username}>"


class Article(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255))
    author      = db.Column(db.String(100))
    body        = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=db.func.now())
    updated_at  = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<Article {self.title}, {self.author}>"

    def __str__(self):
        return f"<Article {self.title}, {self.author}>"
