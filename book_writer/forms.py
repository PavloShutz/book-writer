from flask import Markup
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, TextAreaField
)
from wtforms.validators import DataRequired

from .constants import GENRES


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class BookEditingForm(FlaskForm):
    """Edit book in book editor."""
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
    """Publish book rating."""
    label = Markup('<label class="label">{}</label>')
    rate = SelectField(
        label=label.format("Rate this book"), choices=[
            (i, str(i)) for i in range(1, 6)
        ]
    )
