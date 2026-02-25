import os
import pytest

from backend.flask_api.DBmodel import User


def test_user_list(user_admin_headers, client):
    response = client.get("/users", headers=user_admin_headers)
    assert response.status_code == 200
    assert response.get_json()["users"]


def test_get_user_not_found(user_admin_headers, client):
    response = client.get("/user/9999", headers=user_admin_headers)
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("username", "password", "access_level"),
    (
        ("test_user_2", "test1", 1),
        ("test_study_admin_2", "test2", 2),
    ),
)
def test_user_creation(app, user_admin_headers, client, username, password, access_level):
    response = client.post(
        "/user",
        json={
            "username": username,
            "password": password,
            "access_level": access_level,
        },
        headers=user_admin_headers,
    )
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user is not None
        if access_level == 2:
            assert os.path.isdir(os.path.join(app.config["IMAGE_PATH"], str(user.id)))


@pytest.mark.parametrize(
    ("username", "password", "access_level", "message"),
    (
        ("", "test4", 1, "Username is required."),
        ("test_study_admin_creation", "", 2, "Password is required."),
        ("uadmin", "test6", 3, "already registered"),
    ),
)
def test_user_creation_input_validation(
    user_admin_headers, client, username, password, access_level, message
):
    response = client.post(
        "/user",
        json={
            "username": username,
            "password": password,
            "access_level": access_level,
        },
        headers=user_admin_headers,
    )
    assert response.status_code == 400
    assert message in response.get_json()["error_msg"]


def test_user_modification(app, user_admin_headers, client):
    response = client.post(
        "/user",
        json={"username": "mod_user", "password": "test", "access_level": 1},
        headers=user_admin_headers,
    )
    user_id = response.get_json()["user"]["id"]

    response = client.put(
        f"/user/{user_id}",
        json={"username": "mod_user_new", "password": "new", "access_level": 2},
        headers=user_admin_headers,
    )
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(id=user_id).first()
        assert user.username == "mod_user_new"
        assert user.access_level == 2


def test_user_modification_permission_denied(user_admin_headers, client):
    response = client.put(
        "/user/3",
        json={"username": "blocked", "password": "new", "access_level": 2},
        headers=user_admin_headers,
    )
    assert response.status_code == 401
    assert "Permission denied" in response.get_json()["error_msg"]


def test_user_deletion(user_admin_headers, client):
    response = client.post(
        "/user",
        json={"username": "del_user", "password": "test", "access_level": 1},
        headers=user_admin_headers,
    )
    user_id = response.get_json()["user"]["id"]

    response = client.delete(f"/user/{user_id}", headers=user_admin_headers)
    assert response.status_code == 200


def test_user_deletion_denied(user_admin_headers, client):
    response = client.delete("/user/3", headers=user_admin_headers)
    assert response.status_code == 401
