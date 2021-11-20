import pytest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post

class TestModels:
    @classmethod
    def set_up(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
        db.create_all()
        assert len(User.query.all()) == 0
        assert len(Post.query.all()) == 0

    @classmethod
    def tear_down(cls):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        TestModels.set_up()
        self.u = User(username='Admin')
        self.u.set_password('foo')
        assert self.u.check_password('foo') == True
        assert self.u.check_password('bar') == False
        TestModels.tear_down()

    def test_avatar(self):
        TestModels.set_up()
        self.u = User(username='Admin', email='admin@example.com')
        # import pdb; pdb.set_trace()
        split = self.u.avatar(128).split('/')
        assert split[0] == 'https:'
        assert split[2] == 'www.gravatar.com'
        assert split[3] == 'avatar'
        assert '?d=identicon&s=128' in split[-1]
        TestModels.tear_down()
