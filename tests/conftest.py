import pytest
from app.models import User

@pytest.fixture(scope='function')
def dummy_user():
    user = User(
        username='Admin',
        email='admin@example.com',
        about_me='What up!'
    )
    user.set_password('guest')
    return user

# TODO: add vcrpy package to requirements when external API calls are integrated
# @pytest.fixture(scope='module')
# def vcr_config():
#     return {
#         # Replace the Authorization request header with "DUMMY" in cassettes:
#         "filter_headers": [('authorization', 'DUMMY')],
#         "filter_query_parameters": [('key', 'DUMMY')],
#         "filter_post_data_parameters": [('key', 'DUMMY')]
#     }
