"""Establish connection with database."""

import sqlite3

import click
from flask import current_app, g


def get_db():
    """Return the connection to the database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Terminate the connection with database after before sending response."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Call `close_db` function when cleaning up after returning the response.\n
    Add new command that can be called with the `flask` command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
