from app import app, db
from app.models import User, Post, Message
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.forms import EditProfileForm, EmptyForm, PostForm, SearchForm, WeatherReportForm, MessageForm
from app.email import send_password_reset_email
from app.weather import Weather
from datetime import datetime
from flask import g, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
        g.weather = Weather()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# decorator that protects app (function call) from unauthenticated ('anonymous') current_user
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        posts = current_user.followed_posts().paginate(
            page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('index', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('index', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('main/index.html', title='Home', form=form,
                               posts=posts.items, next_url=next_url, prev_url=prev_url)
    return render_template('main/index.html', title='Home', form=form)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.created_at.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('explore', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('explore', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('main/index.html', title='Explore', posts=posts.items,
                               next_url=next_url, prev_url=prev_url)
    return render_template('main/index.html', title='Explore')

@app.route('/search', methods=['GET'])
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    posts = Post.search(request.args['q']).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('search', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('search', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html', title='Search', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
    form = WeatherReportForm()
    if form.validate_on_submit():
        location = Weather.sanitize_request_params(form.city.data, form.state.data)
        if g.weather.get_forecast(location) == Weather.api_error():
            flash('Sorry! The weather API is currently unavailable, please try again later.')
        flash(f'Now showing weather reports for: {Weather.reformat_input_location(location)}')
        return render_template('main/weather.html', title='Weather Report',
                        location=location,
                        conditions=g.weather.conditions(),
                        current_temp=g.weather.current_temp(),
                        feels_like=g.weather.feels_like(),
                        humidity=g.weather.humidity(),
                        uvi=g.weather.uvi(),
                        avg_hourly=g.weather.avg_hourly_temp(),
                        median_hourly=g.weather.median_hourly_temp(),
                        hourly_conditions=g.weather.forecasted_conditions('hourly'),
                        avg_daily_highs=g.weather.avg_daily_highs(),
                        avg_daily_lows=g.weather.avg_daily_lows(),
                        daily_conditions=g.weather.forecasted_conditions('daily'))
    return render_template('main/weather.html', title='Weather Report', form=form)

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('main/send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    if current_user.is_authenticated:
        current_user.last_message_read_time = datetime.utcnow()
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        messages = current_user.messages_received.order_by(
            Message.created_at.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('messages', page=messages.next_num) \
            if messages.has_next else None
        prev_url = url_for('messages', page=messages.prev_num) \
            if messages.has_prev else None
        return render_template('main/messages.html', messages=messages.items,
                               next_url=next_url, prev_url=prev_url)
    return render_template('main/messages.html')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.created_at.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('main/user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_authenticated:
        form = EditProfileForm(current_user.username)
        if form.validate_on_submit():
            current_user.username = User.clean_username(form.username.data)
            current_user.about_me = form.about_me.data
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user',
                            username=User.clean_username(form.username.data)))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('main/edit_profile.html', title='Edit Profile',
                               form=form)
    form = EditProfileForm('')
    return render_template('main/edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User "{username}" not found.')
            return redirect(url_for('index'))
        if 'follow' in request.args.getlist('action'):
            if user == current_user:
                flash('You cannot follow yourself!')
                return redirect(url_for('user', username=username))
            current_user.follow(user)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'You are now following {username}!')
        elif 'unfollow' in request.args.getlist('action'):
            if user == current_user:
                flash('You cannot unfollow yourself!')
                return redirect(url_for('user', username=username))
            current_user.unfollow(user)
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            flash(f'You are no longer following {username}.')
        return redirect(url_for('user', username=username))
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=User.clean_username(form.username.data),
                    email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for joining the party, fellow Shred-head!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # determine if URL is relative vs absolute, and parse with Werkzeug.url_parse()
            # (to check if netloc component is set):
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Welcome back, fellow Shred-head!')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)
