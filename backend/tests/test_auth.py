import pytest

from backend.flask_api.DBmodel import User


def test_register_success(client, app):
    response = client.post(
        "/auth/register",
        json={"username": "test_user_register", "password": "test"},
    )
    assert response.status_code == 200

    with app.app_context():
        assert User.query.filter_by(username="test_user_register").first() is not None


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", "Username is required."),
        ("test", "", "Password is required."),
        ("user", "user", "already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert response.status_code == 401
    assert message in response.get_json()["error_msg"]


@pytest.mark.parametrize(
    ("username", "password", "role"),
    (
        ("user", "user", "study_participant"),
        ("sadmin", "sadmin", "study_admin"),
        ("uadmin", "uadmin", "user_admin"),
    ),
)
def test_login_success(client, username, password, role):
    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["role"] == role
    assert payload["accessToken"]


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("missing", "user", "Incorrect username."),
        ("user", "bad", "Incorrect password"),
    ),
)
def test_login_validate_input(client, username, password, message):
    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 401
    assert message in response.get_json()["error_msg"]


def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
