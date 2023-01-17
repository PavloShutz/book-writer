from flask import Markup
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    TextAreaField,
    SubmitField,
    EmailField
)
from wtforms.validators import DataRequired, Email

from .constants import GENRES


class LoginForm(FlaskForm):
    username_or_email = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()


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
    submit = SubmitField()
