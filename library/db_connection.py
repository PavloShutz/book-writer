import sqlite3
from flask import g
from library import app

DATABASE = 'library.db'


def get_db():
    """Access db."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Terminate connection with db."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
