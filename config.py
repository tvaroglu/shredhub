import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://')
    if os.environ.get('DOCKER_ENV', '') != '':
        POSTGRES_DB       = os.environ['POSTGRES_DB']
        POSTGRES_HOST     = os.environ['POSTGRES_HOST']
        POSTGRES_USER     = os.environ['POSTGRES_USER']
        POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
        POSTGRES_PORT     = os.environ['POSTGRES_PORT']
        SQLALCHEMY_DATABASE_URI = \
            f"{DATABASE_URL.split('//')[0]}//{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = [MAIL_DEFAULT_SENDER]
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
