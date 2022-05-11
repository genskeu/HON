import pytest
import sys
sys.path.append('../HON')

from backend import create_app
from backend.DBmodel import *

# general create test config file (copy config)
# persistent db might be a better and more realisitc setting?
# other option write more complex tests

# switch local host to something more generic!

# read in SQL for populating test data
@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()        
    
    # init db before running tests
    with app.app_context():
        init_db()
        init_img_dir()
        add_default_users()

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
