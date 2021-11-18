from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# see docs for more detail on .from_object() function:
# https://www.kite.com/python/docs/flask.Config.from_object
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# import routes at END of file to prevent circular imports
from app import routes, models
