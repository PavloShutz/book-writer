from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class BookEditorForm(FlaskForm):
    title = StringField(
        'Book title',
        validators=[DataRequired(message="Please, DO IT!"), Length(max=55)],
    )
    content = TextAreaField(
        'Your content',
        validators=[DataRequired(), Length(min=100)],
    )
    author = StringField(
        'Author',
        validators=[DataRequired(), Length(max=20)]
    )
    genre = SelectField(
        u'Book genre',
        choices=[
            ('fantasy', 'fantasy'),
            ('history', 'history'),
            ('graphic novel', 'graphic novel'),
            ('home and garden', 'home and garden'),
            ('historical fiction', 'historical fiction'),
            ('humor', 'humor'),
            ('horror', 'horror'),
            ('journal', 'journal'),
        ]
    )
