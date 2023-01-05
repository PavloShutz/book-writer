import os

from flask import current_app


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = "YOUR SECRET KEY HERE"
    DATABASE = os.path.join(current_app.instance_path, 'book_writer.sqlite')
Gs1goHDCHPVqng3zdZwl6w