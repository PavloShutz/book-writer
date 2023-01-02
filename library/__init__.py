from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = "Hop4key2un-"

from library import routes
