import os
from secrets import token_hex

from flask import current_app


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = token_hex()
    DATABASE = os.path.join(current_app.instance_path, 'book_writer.sqlite')
    WTF_CSRF_SECRET_KEY = token_hex()
