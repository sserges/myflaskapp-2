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