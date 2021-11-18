from flask import Flask
from config import Config

app = Flask(__name__)
# see docs for more detail on .from_object() function:
# https://www.kite.com/python/docs/flask.Config.from_object
app.config.from_object(Config)
# import routes at END of file to prevent circular imports
from app import routes
