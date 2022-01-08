from app import app, db, mail
# from flask_mail import Message
from app.models import User, Post, Message
# decorator to register the function as a shell context function, to auto-import modules for db manipulation
# return dict (vs list) to provide a name under which each obj is referenced in the shell (via dict keys):
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'mail': mail, 'User': User, 'Post': Post, 'Message': Message, 'seed': seed}

def seed():
    imports = {'db': db, 'User': User, 'Post': Post, 'Message': Message}
    users = User.query.all()
    posts = Post.query.all()
    messages = Message.query.all()

    for u in users:
        db.session.delete(u)
    for p in posts:
        db.session.delete(p)
    for m in messages:
        db.session.delete(m)
    db.session.commit()
