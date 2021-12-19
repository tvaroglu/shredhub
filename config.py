import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    # class variable defined for CSRF protection within Flask-WTF (form) extension package
    # TODO: update 2nd expression during deployment process
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = [MAIL_DEFAULT_SENDER]
