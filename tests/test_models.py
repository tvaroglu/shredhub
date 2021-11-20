import pytest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post

class TestModels:
    @classmethod
    def set_up(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
        db.create_all()
        users = User.query.all()
        posts = Post.query.all()
        if len(users) > 0 or len(posts) > 0:
            for u in users:
                db.session.delete(u)
            for p in posts:
                db.session.delete(p)
            db.session.commit()
        assert len(User.query.all()) == 0
        assert len(Post.query.all()) == 0

    @classmethod
    def tear_down(cls):
        db.session.remove()
        db.drop_all()

    @classmethod
    def dummy_user(cls):
        cls.user = User(
            username='Admin',
            email='admin@example.com',
            about_me='What up!'
        )
        return cls.user

    def test_attributes(self):
        TestModels.set_up()
        self.user = TestModels.dummy_user()
        db.session.add(self.user)
        db.session.commit()
        assert len(User.query.all()) == 1
        assert isinstance(self.user, User)
        assert self.user.username == 'Admin'
        assert self.user.email == 'admin@example.com'
        assert self.user.about_me == 'What up!'
        assert isinstance(self.user.created_at, datetime)
        assert isinstance(self.user.updated_at, datetime)
        assert isinstance(self.user.last_seen, datetime)
        TestModels.tear_down()

    def test__repr__(self):
        TestModels.set_up()
        self.user = TestModels.dummy_user()
        assert self.user.__repr__() == f'<User: {self.user.username}>'
        TestModels.tear_down()

    def test_password_hashing(self):
        TestModels.set_up()
        self.user = TestModels.dummy_user()
        self.user.set_password('foo')
        assert self.user.check_password('foo') == True
        assert self.user.check_password('bar') == False
        TestModels.tear_down()

    def test_avatar(self):
        TestModels.set_up()
        self.user = TestModels.dummy_user()
        split = self.user.avatar(128).split('/')
        assert split[0] == 'https:'
        assert split[2] == 'www.gravatar.com'
        assert split[3] == 'avatar'
        assert '?d=identicon&s=128' in split[-1]
        TestModels.tear_down()

    def test_follow(self):
        TestModels.set_up()
        self.user_1 = TestModels.dummy_user()
        self.user_2 = User(username='guest', email='guest@example.com')
        db.session.add(self.user_1)
        db.session.add(self.user_2)
        db.session.commit()
        assert self.user_1.followed.all() == []
        assert self.user_2.followed.all() == []

        self.user_1.follow(self.user_2)
        db.session.commit()
        assert self.user_1.is_following(self.user_2) == True
        assert self.user_1.followed.count() == 1
        assert self.user_1.followed.first().username == self.user_2.username
        assert self.user_2.is_following(self.user_1) == False
        assert self.user_2.followers.count() == 1
        assert self.user_2.followers.first().username == self.user_1.username

        self.user_1.unfollow(self.user_2)
        db.session.commit()
        assert self.user_1.is_following(self.user_2) == False
        assert self.user_1.followed.count() == 0
        assert self.user_2.followers.count() == 0
        TestModels.tear_down()
