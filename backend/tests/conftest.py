import pytest
import sys
sys.path.append('/home/')  # Add backend to path for imports
from backend.flask_api import create_app
from backend.flask_api.DBmodel import add_default_users, init_db, init_img_dir

# general create test config file (copy config)
# persistent db might be a better and more realisitc setting?
# other option write more complex tests

# switch local host to something more generic!

# read in SQL for populating test data
@pytest.fixture
def app(tmp_path):
    """Create and configure a new app instance for each test."""
    app = create_app(
        config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-key",
            "IMAGE_PATH": str(tmp_path / "images"),
        }
    )

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


@pytest.fixture
def auth_headers(client):
    def _login(username, password):
        response = client.post(
            "/auth/login", json={"username": username, "password": password}
        )
        assert response.status_code == 201
        token = response.get_json()["accessToken"]
        return {"Authorization": f"Bearer {token}"}

    return _login


@pytest.fixture
def study_admin_headers(auth_headers):
    return auth_headers("sadmin", "sadmin")


@pytest.fixture
def user_admin_headers(auth_headers):
    return auth_headers("uadmin", "uadmin")


@pytest.fixture
def participant_headers(auth_headers):
    return auth_headers("user", "user")
