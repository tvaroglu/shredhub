from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        # return '<User {}>'.format(self.username)
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        # return '<Post {}>'.format(self.body)
        return f'<Post {self.body}>'
