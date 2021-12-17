import pytest
import json
import pprint
pp = pprint.PrettyPrinter(indent=2)
from app import db
import flask
from flask_login import login_user, logout_user, current_user

class TestRoutes:
    @classmethod
    def set_up(cls, test_app):
        with test_app.test_client() as client:
            yield client

    @classmethod
    def tear_down(cls, test_app):
        db.session.remove()
        db.drop_all()

    def test_registration(self, test_app):
        self.generator = TestRoutes.set_up(test_app)
        self.client = next(self.generator)
        self.request = self.client.get('/register')
        assert self.request.status_code == 200
        self.response = str(self.request.data)
        assert 'Registration' in self.response
        assert 'Username' in self.response
        assert 'Password' in self.response
        assert 'Confirm Password' in self.response
        assert 'Register' in self.response
        TestRoutes.tear_down(test_app)

    def test_login(self, test_app):
        self.generator = TestRoutes.set_up(test_app)
        self.client = next(self.generator)
        self.request = self.client.get('/login')
        assert self.request.status_code == 200
        self.response = str(self.request.data)
        assert 'Login' in self.response
        assert 'Email' in self.response
        assert 'Password' in self.response
        assert 'Remember Me' in self.response
        assert 'Sign In' in self.response
        TestRoutes.tear_down(test_app)

    def test_404(self, test_app):
        self.generator = TestRoutes.set_up(test_app)
        self.client = next(self.generator)
        self.request = self.client.get('/foo_bar')
        assert self.request.status_code == 404
        self.response = str(self.request.data)
        assert 'Page Not Found.. Perhaps Your Trail Map is Upside Down?' in self.response
        TestRoutes.tear_down(test_app)

    def test_current_user(self, test_app, dummy_user):
        self.user = dummy_user
        login_user(self.user, remember=True)
        assert current_user.username == self.user.username
        assert current_user.email == self.user.email
        assert current_user.is_authenticated == True
        logout_user()
        assert current_user.is_authenticated == False
        TestRoutes.tear_down(test_app)

    def test_index_path(self, test_app, dummy_user):
        with test_app.test_request_context('/index'):
            login_user(dummy_user, remember=True)
            assert flask.request.path == '/index'
        TestRoutes.tear_down(test_app)

    def test_index(self, test_app, dummy_user):
        self.generator = TestRoutes.set_up(test_app)
        self.client = next(self.generator)
        self.request = self.client.get('/index')
        assert self.request.status_code == 200
        self.response = str(self.request.data)
        assert 'Where&#39;s the powder at today?' in self.response
        assert 'Submit' in self.response
        TestRoutes.tear_down(test_app)
