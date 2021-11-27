import pytest
import json
import pprint
pp = pprint.PrettyPrinter(indent=2)
from app import app, db
from app.models import User, Post
from flask_login import login_user, logout_user, current_user

class TestRoutes:
    @classmethod
    def set_up(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                # TODO: Figure out the proper way to mock flask_login user auth..
                # can't get contexts to be remembered across tests, or even single requests via test_client()
                # TestRoutes.test_login_user(client)
            return client

    @classmethod
    def tear_down(cls):
        db.session.remove()
        db.drop_all()

    @classmethod
    def test_login_user(cls, client, email='Admin@example.com', username='Admin', password='guest'):
        user = User(email=email, username=username, password_hash=password)
        client.post('/login', data=dict(
            email=user.email,
            password=user.password_hash
        ), follow_redirects=True)
        login_user(user, remember=True)
        assert current_user.username == user.username
        assert current_user.email == user.email

    def test_registration(self):
        self.client = TestRoutes.set_up()
        self.request = self.client.get('/register')
        assert self.request.status_code == 200
        self.response = str(self.request.data)
        assert 'Registration' in self.response
        assert 'Username' in self.response
        assert 'Password' in self.response
        assert 'Confirm Password' in self.response
        assert 'Register' in self.response
        TestRoutes.tear_down()

    def test_404(self):
        self.client = TestRoutes.set_up()
        self.request = self.client.get('/foo_bar')
        assert self.request.status_code == 404
        self.response = str(self.request.data)
        assert 'Page Not Found.. Perhaps Your Trail Map is Upside Down?' in self.response
        TestRoutes.tear_down()

    def test_index(self):
        self.client = TestRoutes.set_up()
        assert str(type(self.client)) == "<class 'flask.testing.FlaskClient'>"
        # self.request = self.client.get('/')
        # import pdb; pdb.set_trace()
        # assert self.request.status_code == 200
        # assert self.request.location == '/'
        TestRoutes.tear_down()
