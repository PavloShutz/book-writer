from flask import (
    Blueprint,
    render_template
)
from .db import get_db

bp = Blueprint('users', __name__)


@bp.route("/users")
def show_users():
    db = get_db()
    users = {}
    query = db.execute("""
    SELECT rating, username FROM book JOIN user ON book.author_id = user.id
    """).fetchall()
    for user in query:
        if user['username'] not in users.keys():
            users[user['username']] = user['rating']
        else:
            users[user['username']] = (
                    users[user['username']] + user['rating']
            ) / 2
    return render_template('book/users.html', users=users)