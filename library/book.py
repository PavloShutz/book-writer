from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.exceptions import abort

from library.auth import login_required
from library.db import get_db

bp = Blueprint('book', __name__)


@bp.route('/')
def index():
    db = get_db()
    books = db.execute(
        'SELECT b.id, title, content, created, genre, author_id, username'
        ' FROM book b JOIN user u ON b.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('book/index.html', books=books)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        print(request.form.get('genre'))
        genre = request.form['genre']
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

    return render_template('book/create.html')


def get_book(id, check_author=True, read_mode=False):
    book = get_db().execute(
        'SELECT b.id, title, content, created, genre, author_id, username'
        ' FROM book b JOIN user u ON b.author_id = u.id'
        ' WHERE b.id = ?',
        (id,)
    ).fetchone()

    if book is None:
        abort(404, "Post id {0} doesn't exists".format(id))

    if not read_mode:
        if check_author and book['author_id'] != g.user['id']:
            abort(403)

    return book


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    book = get_book(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['content']
        genre = request.form['genre']
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
                (title, body, genre, id)
            )
            db.commit()
            return redirect(url_for('book.index'))
    return render_template('book/book_editing.html', book=book)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_book(id)
    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('book.index'))


@bp.route('/read/<int:id>')
def read(id):
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    book = get_book(id, read_mode=True)
    return render_template('book/read_book.html', book=book)
