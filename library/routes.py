from flask import render_template, redirect, url_for, request

from library import app
from library.db_connection import get_db
from library.forms import BookEditorForm


@app.route('/')
@app.route('/index')
def index():
    """Home page."""
    cur = get_db().cursor()
    books = cur.execute("SELECT id, title, author, genre, content FROM books").fetchall()
    return render_template('index.html', books=books)


def post_book(title, content, author, genre) -> None:
    """Add new book to table."""
    con = get_db()
    con.execute('INSERT INTO books(title, author, genre, content) VALUES(?, ?, ?, ?)',
                (title, author, genre, content))
    con.commit()
    con.close()


@app.route('/write_book', methods=['POST', 'GET'])
def write_book():
    """Edit and publish book."""
    form = BookEditorForm()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        genre = request.form['genre']
        post_book(title, content, author, genre)
        return redirect(url_for('index'))
    return render_template('book_editing.html', form=form)


@app.route('/read_book/<int:book_id>')
def read_book(book_id: int):
    cur = get_db().cursor()
    info = cur.execute("SELECT id, title, author, genre, content FROM books WHERE id=%s" % book_id).fetchone()
    return render_template('read_book.html', info=info)
