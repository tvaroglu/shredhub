from flask import render_template
from app import app
from app.forms import LoginForm

# View functions with decorators added to create an association between the URL (arg) and associated function call:
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
