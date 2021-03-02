import pytest
from flask import g
from flask import session
from TAFC.DBmodel import User 


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get("/auth/register").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/auth/register", data={"username": "test_user_register", "password": "test"})
    assert "http://localhost/auth/login" == response.headers["Location"]

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            User.query.filter_by(username="test_user_register").first()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("test", "", b"Password is required."),
        ("default_user", "user", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data

@pytest.mark.parametrize(
    ("username", "password", "location","id"),
    (("default_user", "user", "http://localhost/study/login",1), 
     ("default_study_admin", "study_admin", "http://localhost/studies/overview",2),
     ("default_user_admin", "user_admin", "http://localhost/users/overview",3))
)
def test_login(client, auth,username, password,location,id):
    # test that viewing the page renders without template errors
    assert client.get("/auth/login").status_code == 200

    # test that successful login redirects to the index page
    response = auth.login(username,password)
    assert response.headers["Location"] == location

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["user_id"] == id
        assert g.user.username == username


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "user", b"Incorrect username."), ("default_user", "a", b"Incorrect password.")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

@pytest.mark.parametrize(
    ("username", "password"),
    (("default_user", "user"), 
     ("default_study_admin", "study_admin"),
     ("default_user_admin", "user_admin"))
)
def test_logout(client, auth,username,password):
    auth.login(username,password)

    with client:
        auth.logout()
        assert "user_id" not in session

urls = (("/",[2]),
        ("/study/login",[1,2]),
        ("/studies/overview",[2]),
        ("/study/create",[2]),
        ("/study/login",[1,2]),
        ("/results/overview",[2]),
        ("/users/overview",[3]),
        ("/user/create",[3]),
        ("/user/modify/1",[3]),
        ("/profile",[1,2,3]))

@pytest.mark.parametrize(
    ("url","access_level_required"),
    (urls)
)
def test_login_required(client,url,access_level_required):
    response = client.get(url)
    assert "http://localhost/auth/login" == response.headers["Location"]

@pytest.mark.parametrize(
    ("url","access_level_required"),
    (urls)
)
@pytest.mark.parametrize(
    ("username","password","access_level","redirect"),
    (("default_user", "user",1, "http://localhost/study/login"), 
     ("default_study_admin", "study_admin",2, "http://localhost/studies/overview"),
     ("default_user_admin", "user_admin",3, "http://localhost/users/overview"))
)

def test_access_level_required(client,auth,url,access_level_required,username,password,access_level,redirect):
    auth.login(username,password)
    response = client.get(url)
    if access_level in access_level_required:
        assert response.status_code == 200
    else:
        assert response.headers["Location"] == redirect
