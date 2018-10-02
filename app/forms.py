from wtforms import (
    Form,
    StringField,
    TextAreaField,
    PasswordField
)
from wtforms.validators import (
    Length,
    Email,
    DataRequired,
    EqualTo
)
from passlib.hash import sha256_crypt

class RegisterForm(Form):
    name = StringField('Name', [DataRequired(), Length(min=1, max=50)])
    username = StringField('Username', [DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', [Email()])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [DataRequired()])


class ArticleForm(Form):
    title = StringField('Title', [DataRequired(), Length(min=1, max=200)])
    body = TextAreaField('Body', [DataRequired(), Length(min=30)])
