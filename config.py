import os

class Config(object):
    # class variable defined for CSRF protection within Flask-WTF (form) extension package
    # TODO: update 2nd expression during deployment process
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
