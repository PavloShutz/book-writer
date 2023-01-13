"""Book writer with ```create_app``` application factory."""

import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        with app.app_context():
            app.config.from_object('config.Config')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, auth, book
    # registering application
    db.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    # registering blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(book.bp)
    app.add_url_rule('/', endpoint='index')

    return app
