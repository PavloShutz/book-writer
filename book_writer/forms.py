from flask import Markup
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, TextAreaField
)
from wtforms.validators import DataRequired, EqualTo

from .constants import GENRES


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
        DataRequired(), EqualTo('confirm', message='Passwords must match!')
    ])

class BookEditingForm(FlaskForm):
    label = Markup('<label class="label">{}</label>')
    title = StringField(
        label=label.format("Title"), validators=[DataRequired()]
    )
    genre = SelectField(
        label=label.format("Genre"),
        choices=[(genre, genre) for genre in GENRES]
    )
    content = TextAreaField(
        label=label.format("Content")
    )


class RateForm(FlaskForm):
    label = Markup('<label class="label">{}</label>')
    rate = SelectField(
        label=label.format("Rate this book"), choices=[
            (i, str(i)) for i in range(1, 6)
        ]
    )
