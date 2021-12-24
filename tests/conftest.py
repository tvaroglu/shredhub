import pytest
from app import app, db
from app.models import User

@pytest.fixture(scope='function')
def test_app():
    app.config['TESTING'] = True
    # disable @login_required decorator for unittesting:
    app.config['LOGIN_DISABLED'] = True
    # change app config to use an in-memory version of db:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture(scope='function')
def dummy_user():
    user = User(
        username='Admin',
        email='admin@example.com',
        about_me='What up!'
    )
    user.set_password('guest')
    return user

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace any Authorization request headers with 'DUMMY' in cassettes:
        'filter_headers': [('authorization', 'DUMMY')],
        'filter_query_parameters': [('key', 'DUMMY')],
        'filter_post_data_parameters': [('key', 'DUMMY')]
    }
