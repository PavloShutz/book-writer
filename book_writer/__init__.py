"""Book writer with ```create_app``` application factory
and basic logging config."""

import os
from logging.config import dictConfig

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s]--[%(module)s]--[%(levelname)s]--[%(message)s]',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi'],
    }
})


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

    from . import db, auth, book, users
    # registering application
    db.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    bootstrap = Bootstrap5()
    bootstrap.init_app(app)
    # registering blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')
    from .http_errors import \
        page_not_found, internal_server_error
    # register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app
