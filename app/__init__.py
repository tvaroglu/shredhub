from flask import Flask
app = Flask(__name__)
# import routes at END of file to prevent circular imports
from app import routes
