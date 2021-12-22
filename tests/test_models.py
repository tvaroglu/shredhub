import pytest
from datetime import datetime, timedelta
from app import db
from app.models import User, Post, load_user

class TestModels:
    @classmethod
    def set_up(cls, test_app):
        if len(User.query.all()) > 0 or len(Post.query.all()) > 0:
            for u in User.query.all():
                db.session.delete(u)
            for p in Post.query.all():
                db.session.delete(p)
            db.session.commit()

    @classmethod
    def tear_down(cls, test_app):
        db.session.remove()
        db.drop_all()

    def test_user_attributes(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        db.session.add(self.user)
        db.session.commit()
        assert len(User.query.all()) == 1
        assert isinstance(self.user, User)
        assert self.user.username == 'Admin'
        assert self.user.email == 'admin@example.com'
        assert self.user.about_me == 'What up!'
        assert isinstance(self.user.password_hash, str)
        assert isinstance(self.user.created_at, datetime)
        assert isinstance(self.user.updated_at, datetime)
        assert isinstance(self.user.last_seen, datetime)
        TestModels.tear_down(test_app)

    def test__repr__(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        assert self.user.__repr__() == f'<User: {self.user.username}>'
        TestModels.tear_down(test_app)

    def test_load_user(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        db.session.add(self.user)
        db.session.commit()
        self.user_loader = load_user(self.user.id)
        assert self.user_loader.id == self.user.id
        assert self.user_loader.username == self.user.username
        assert self.user_loader.about_me == self.user.about_me
        assert self.user_loader.password_hash == self.user.password_hash
        TestModels.tear_down(test_app)

    def test_password_hashing(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        assert self.user.check_password('guest') == True
        assert self.user.check_password('foo') == False
        TestModels.tear_down(test_app)

    def test_avatar(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        split = self.user.avatar(128).split('/')
        assert split[0] == 'https:'
        assert split[2] == 'www.gravatar.com'
        assert split[3] == 'avatar'
        assert '?d=identicon&s=128' in split[-1]
        TestModels.tear_down(test_app)

    def test_follow(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user_1 = dummy_user
        self.user_2 = User(username='Guest', email='guest@example.com')
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
        TestModels.tear_down(test_app)

    def test_post_attributes(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        now = datetime.utcnow()
        self.post = Post(body='test post', author=self.user, created_at=now)
        assert self.post.__repr__() == f'<Post: {self.post.body}>'
        db.session.add(self.user)
        db.session.add(self.post)
        db.session.commit()
        assert len(Post.query.all()) == 1
        assert isinstance(self.post, Post)
        assert self.post.body == 'test post'
        assert self.post.user_id == self.user.id
        assert isinstance(self.post.created_at, datetime)
        TestModels.tear_down(test_app)

    def test_followed_posts(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        # create four users:
        self.user_1 = dummy_user
        self.user_2 = User(username='Guest', email='guest@example.com')
        self.user_3 = User(username='Mary', email='mary@example.com')
        self.user_4 = User(username='David', email='david@example.com')
        db.session.add_all([self.user_1, self.user_2, self.user_3, self.user_4])
        # create four posts:
        now = datetime.utcnow()
        self.post_1 = Post(body='post from Admin', author=self.user_1,
                  created_at=now + timedelta(seconds=1))
        self.post_2 = Post(body='post from Guest', author=self.user_2,
                  created_at=now + timedelta(seconds=4))
        self.post_3 = Post(body='post from Mary', author=self.user_3,
                  created_at=now + timedelta(seconds=3))
        self.post_4 = Post(body='post from David', author=self.user_4,
                  created_at=now + timedelta(seconds=2))
        db.session.add_all([self.post_1, self.post_2, self.post_3, self.post_4])
        db.session.commit()
        # set up the followers:
        self.user_1.follow(self.user_2)  # Admin follows Guest
        self.user_1.follow(self.user_4)  # Admin follows David
        self.user_2.follow(self.user_3)  # Guest follows Mary
        self.user_3.follow(self.user_4)  # Mary follows David
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
        TestModels.tear_down(test_app)

    def test_password_reset_token(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        assert User.verify_password_reset_token('foo') == None
        db.session.add(self.user)
        db.session.commit()
        self.token = self.user.get_password_reset_token()
        assert isinstance(self.token, str)
        assert User.verify_password_reset_token(self.token) == self.user
        TestModels.tear_down(test_app)

    def test_clean_username(self, test_app):
        TestModels.set_up(test_app)
        self.bad_username = 'Admin/\\'
        assert User.clean_username(self.bad_username) == 'Admin'

    def test_post_search(self, test_app, dummy_user):
        TestModels.set_up(test_app)
        self.user = dummy_user
        now = datetime.utcnow()
        self.post_1 = Post(body='post from admin', author=self.user,
                  created_at=now + timedelta(seconds=1))
        self.post_2 = Post(body='another post from Admin', author=self.user,
                  created_at=now + timedelta(seconds=2))
        self.post_3 = Post(body='another POST FROM ADMIN', author=self.user,
                  created_at=now + timedelta(seconds=3))
        self.post_4 = Post(body='foo bar baz', author=self.user,
                  created_at=now)
        db.session.add_all([self.post_1, self.post_2, self.post_3, self.post_4])
        db.session.commit()
        assert Post.search('post from admin').all() == [self.post_3, self.post_2, self.post_1]
        TestModels.tear_down(test_app)
