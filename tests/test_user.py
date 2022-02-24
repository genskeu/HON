import pytest
import os
from app.DBmodel import User 
from werkzeug.security import check_password_hash
from flask import session


def create_user(client, username, password, access_level):
    response = client.post("/user/create", data={"username": username, "password": password,"access_level":access_level})
    return response


@pytest.mark.parametrize(
    ("username", "password", "access_level"),
    (("test_user_2", "test1", 1), 
     ("test_study_admin_2", "test2", 2),
     ("test_user_admin_2", "test3", 3)),
)
def test_user_creation(app,auth,client,username, password, access_level):
    auth.login("default_user_admin","user_admin")
    response = create_user(client,username, password, access_level)
    assert response.status_code == 302

    # test that the user was inserted into the database
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        assert user is not None
        # if study_admin test if image folder created
        if access_level == 2:
            assert os.path.isdir(os.path.join(app.config["IMAGE_PATH"],str(user.id)))



@pytest.mark.parametrize(
    ("username", "password", "access_level","message"),
    (("", "test4", 1, b"Username is required."), 
     ("test_study_admin_creation", "", 2, b"Password is required."),
     ("default_user_admin", "test6", 3, b"User default_user_admin is already registered.")),
)

def test_user_creation_input_validation(app,auth,client,username, password, access_level,message):
    auth.login("default_user_admin","user_admin")
    response = create_user(client,username, password, access_level)
    assert message in response.data


def modify_user(client,user_id, username, password, access_level):
    response = client.post("/user/modify/" + user_id, data={"username": username, "password": password,"access_level":access_level})
    return response


@pytest.mark.parametrize(
    ("user_id", "username", "password", "access_level"),
    (("1","test_user_a", "test7", 3), 
     ("2","test_study_admin_b", "test8", 1),
     ("2","test_study_admin_b", "test8", 2),
     ("3","test_user_admin_c", "test9", 2),
     ("3","", "", 2)),
)
def test_user_modification(app,auth,client,user_id, username, password, access_level):
    auth.login("default_user_admin","user_admin")
    with app.app_context():
        user = User.query.filter_by(id=user_id).first()
    response = modify_user(client,user_id, username, password, access_level)

    assert response.status_code == 302

    # test that the user was modified in the database
    with app.app_context():
        user = User.query.filter_by(id=user_id).first()
        if username:
            assert user.username == username
        if password:
            assert check_password_hash(user.password, password)
        assert user.access_level == access_level

        # if study_admin test if image folder created/renamed
        if access_level == 2:
            assert os.path.isdir(os.path.join(app.config["IMAGE_PATH"],str(user.id)))

@pytest.mark.parametrize(
    ("user_id","username", "password", "access_level","message"),
    (("1","default_user_admin", "test6", 3, b"User default_user_admin is already registered."),),
)

def test_user_modification_input_validation(app,auth,client,user_id, username, password, access_level,message):
    auth.login("default_user_admin","user_admin")
    response = modify_user(client,user_id,username, password, access_level)
    assert message in response.data

def delete_user(client,user_id):
    response = client.delete("/user/modify/" + user_id)
    return response

# to do: delete of user admin not possible
@pytest.mark.parametrize(
    ("user_id", "username", "password", "access_level"),
    (("1","test_user_a", "test7", 3), 
     ("2","test_study_admin", "test2", 2),
     ("3","test_user_admin", "test9", 3)
     ),
)

def test_user_del(app,auth,client,user_id, username,password,access_level):
    auth.login("default_user_admin","user_admin")
    response = delete_user(client,user_id)
    assert response.status_code == 200
   # test that the user was deleted in the database
    with app.app_context():
        user = User.query.filter_by(id=user_id).first() 
        if access_level < 3:
            assert user is None
        else:
            b"Permission denied." in response.data

@pytest.mark.parametrize(
    ("username", "password", "new_username", "new_password"),
    (("default_user", "user", "test_user_rn", "123456"), 
     ("default_study_admin", "study_admin", "study_admin_rn","test2"),
     ("default_user_admin", "user_admin", "test_user_admin_rn","blup")
     ),
)

def test_modify_profile(app,auth,client,username,password,new_username, new_password):
    auth.login(username,password)
    with client:
        response = client.post("/profile", data={"username": new_username, "password": new_password})
        user_id = session["user_id"]
        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(id=user_id).first()
            assert user.username == new_username
            assert check_password_hash(user.password, new_password)

@pytest.mark.parametrize(
    ("new_username", "new_password","message"),
    (("default_user_admin", "test6", b"User default_user_admin is already registered."),),
)
def test_modify_profile_input_validation(app,auth,client,new_username, new_password,message):
    auth.login("default_user","user")
    response = client.post("/profile", data={"username": new_username, "password": new_password})
    assert message in response.data
