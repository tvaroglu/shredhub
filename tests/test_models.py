import pytest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post

class TestModels:
    @classmethod
    def set_up(cls):
        # change app config to use an in-memory version of db:
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

    def test_user_attributes(self):
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

    def test_post_attributes(self):
        TestModels.set_up()
        self.user = TestModels.dummy_user()
        now = datetime.utcnow()
        self.post = Post(body='test post', author=self.user, created_at=now)
        db.session.add(self.user)
        db.session.add(self.post)
        db.session.commit()
        assert len(Post.query.all()) == 1
        assert isinstance(self.post, Post)
        assert self.post.body == 'test post'
        assert self.post.user_id == self.user.id
        assert isinstance(self.post.created_at, datetime)
        TestModels.tear_down()

    def test_followed_posts(self):
        TestModels.set_up()
        # create four users:
        self.user_1 = TestModels.dummy_user()
        self.user_2 = User(username='guest', email='guest@example.com')
        self.user_3 = User(username='mary', email='mary@example.com')
        self.user_4 = User(username='david', email='david@example.com')
        db.session.add_all([self.user_1, self.user_2, self.user_3, self.user_4])
        # create four posts:
        now = datetime.utcnow()
        self.post_1 = Post(body='post from Admin', author=self.user_1,
                  created_at=now + timedelta(seconds=1))
        self.post_2 = Post(body='post from guest', author=self.user_2,
                  created_at=now + timedelta(seconds=4))
        self.post_3 = Post(body='post from mary', author=self.user_3,
                  created_at=now + timedelta(seconds=3))
        self.post_4 = Post(body='post from david', author=self.user_4,
                  created_at=now + timedelta(seconds=2))
        db.session.add_all([self.post_1, self.post_2, self.post_3, self.post_4])
        db.session.commit()
        # set up the followers:
        self.user_1.follow(self.user_2)  # Admin follows guest
        self.user_1.follow(self.user_4)  # Admin follows david
        self.user_2.follow(self.user_3)  # guest follows mary
        self.user_3.follow(self.user_4)  # mary follows david
        db.session.commit()
        # check the followed posts for each user:
        self.followed_posts_1 = self.user_1.followed_posts().all()
        self.followed_posts_2 = self.user_2.followed_posts().all()
        self.followed_posts_3 = self.user_3.followed_posts().all()
        self.followed_posts_4 = self.user_4.followed_posts().all()
        assert self.followed_posts_1 == [self.post_2, self.post_4, self.post_1]
        assert self.followed_posts_2 == [self.post_2, self.post_3]
        assert self.followed_posts_3 == [self.post_3, self.post_4]
        assert self.followed_posts_4 == [self.post_4]
        TestModels.tear_down()
