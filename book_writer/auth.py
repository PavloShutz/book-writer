"""User authentication and authorization."""

import functools

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
from werkzeug.security import \
    check_password_hash, generate_password_hash

from .db import get_db
from .forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


def get_form_data_from_user(form: LoginForm | RegisterForm) -> tuple:
    return form.username.data, form.password.data, form.email.data


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Sign up page"""
    form = RegisterForm()
    if request.method == 'POST':
        username, password, email = get_form_data_from_user(form)
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email)"
                    " VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Sign In page."""
    form = LoginForm()
    if request.method == 'POST':
        username_or_email = form.username_or_email.data
        password = form.password.data
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ? OR email = ?',
            (username_or_email, username_or_email)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """User logs out from this session."""
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """return: wrapper for function that requires login."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
