from flask import (
    Blueprint,
    render_template
)
from .db import get_db

bp = Blueprint('users', __name__)


@bp.route("/users")
def show_users():
    """Show table of users and their data"""
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
    return render_template('users/users.html', users=users)


@bp.route('/profile/<int:user_id>')
def show_user_profile(user_id):
    user = get_db().execute(
        """SELECT username, email,
        COUNT(title) as amount_of_written_books FROM user
        LEFT JOIN book ON book.author_id = user.id WHERE user.id = ?;""",
        (user_id,)).fetchone()
    return render_template("users/profile.html", user=user)
