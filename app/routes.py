from flask import render_template
from app import app
# view functions:
@app.route('/')
@app.route('/index')
def index():
    # TODO: remove mock user and post objects once DB & auth in place
    user = {'username': 'Taylor'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': "Snow's coming this week!"
        },
        {
            'author': {'username': 'Natalie'},
            'body': "Can't wait to check out Steamboat!"
        }
    ]
    # Jinja2 template engine (bundled with Flask) renders content dynamically to templates via passed in args:
    return render_template('index.html', title='Home', user=user, posts=posts)
