from app import app, db
from app.models import User, Post
# decorator to register the function as a shell context function, to auto-import modules for db manipulation:
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
