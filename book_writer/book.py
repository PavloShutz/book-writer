from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_paginate import \
    Pagination, get_page_parameter
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db
from .forms import BookEditingForm, RateForm

bp = Blueprint('book', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 3
    offset = (page - 1) * per_page
    db = get_db()
    total = db.execute("SELECT * FROM book").fetchall()
    books = db.execute(
        'SELECT b.id, title, content, created,'
        ' genre, rating, author_id, username'
        ' FROM book b JOIN user u ON b.author_id = u.id'
        ' ORDER BY created DESC LIMIT ? OFFSET ?', (per_page, offset)
    ).fetchall()
    pagination = Pagination(
        page=page,
        per_page=per_page,
        offset=offset,
        total=len(total),
        search=search,
        record_name='books',
        css_framework='bootstrap5'
    )
    return render_template(
        'book/index.html', books=books, pagination=pagination
    )


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = BookEditingForm()
    if request.method == 'POST':
        title = form.title.data
        content = form.content.data
        genre = form.genre.data
        error = None

        if not title:
            error = 'Title is required.'
        elif not genre:
            error = 'Genre is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (title, content, genre, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, content, genre, g.user['id'])
            )
            db.commit()
            return redirect(url_for('book.index'))

    return render_template('book/create.html', form=form)


def get_book(book_id, check_author=True, read_mode=False):
    book = get_db().execute(
        'SELECT b.id, title, content, created,'
        ' genre, rating, author_id, username'
        ' FROM book b JOIN user u ON b.author_id = u.id'
        ' WHERE b.id = ?',
        (book_id,)
    ).fetchone()

    if book is None:
        abort(404, "Post id {0} doesn't exists".format(id))

    if not read_mode:
        if check_author and book['author_id'] != g.user['id']:
            abort(403)

    return book


def get_genre(book_id):
    db = get_db()
    genre = db.execute(
        "SELECT genre FROM book WHERE id = ?", (book_id,)
    ).fetchone()
    return genre[0]


@bp.route('/<int:book_id>/update', methods=('GET', 'POST'))
@login_required
def update(book_id):
    book = get_book(book_id)
    form = BookEditingForm()
    if request.method == 'POST':
        title = form.title.data
        content = form.content.data
        genre = form.genre.data
        error = None

        if not title:
            error = 'Title is required.'
        elif not genre:
            error = 'Genre is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE book SET title = ?, content = ?, genre = ?'
                ' WHERE id = ?',
                (title, content, genre, book_id)
            )
            db.commit()
            return redirect(url_for('book.index'))
    form.genre.data = get_genre(book_id)
    return render_template('book/book_editing.html', book=book, form=form)


@bp.route('/<int:book_id>/delete', methods=('POST',))
@login_required
def delete(book_id):
    get_book(book_id)
    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (book_id,))
    db.commit()
    return redirect(url_for('book.index'))


def get_rating(book_id):
    db = get_db()
    rating = db.execute(
        "SELECT rating FROM book WHERE id = ?",
        (book_id,)
    ).fetchone()
    return rating[0]


@bp.route('/read/<int:book_id>', methods=("GET", "POST"))
def read(book_id):
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    book = get_book(book_id, read_mode=True)
    rate_form = RateForm()
    if request.method == "POST":
        rating = rate_form.rate.data
        current_rating = get_rating(book_id)
        db = get_db()
        if current_rating == 0:
            db.execute(
                "UPDATE book SET rating = ? WHERE id = ?",
                (rating, book_id)
            )
        else:
            db.execute(
                "UPDATE book SET rating = (rating + ?) / 2 WHERE id = ?",
                (rating, book_id)
            )
        db.commit()
        flash("Thanks for your rating!")
    return render_template('book/read_book.html', book=book, form=rate_form)
