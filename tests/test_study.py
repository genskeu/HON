import pytest
import os
from TAFC.DBmodel import *


def create_study(client,title,description,password):
    response = client.post("/study/create", data={"title": title,
                                                  "description":description, 
                                                  "password": password})
    return response

@pytest.mark.parametrize(
    ("title","description","password"),
    (("test_1","blupblup","test100"),
     ("test_2","","test100"))
)

def test_create_study(app,auth,client,title,description,password):
    auth.login("default_study_admin","study_admin")
    response = create_study(client,title,description,password)
    assert response.status_code == 302
    
    # test that the study was inserted into the database
    with app.app_context():
        study = Study.query.filter_by(title=title).first()
        assert study is not None

        study_dir = study.get_image_dir()
        assert os.path.isdir(study_dir)

@pytest.mark.parametrize(
    ("title","description","password","message"),
    (("test1","blupblup","",b"Password is required."),
     ("","blupblup","test100",b"Title is required."),
     ("test_study_1","blupblup","test",b"Titel already used for a different study. Please choose a different study title."))
)

def test_create_study_input_validation(app,auth,client,title,description,password,message):
    auth.login("default_study_admin","study_admin")
    if title == "test_study_1":
        create_study(client,title,description,password)
    response = create_study(client,title,description,password)
    assert response.status_code == 200
    assert message in response.data



def modifiy_study(client,study_id,title,description,password):
    response = client.post("/study/modify/" + study_id, 
                            data={"title": title,
                                  "description":description, 
                                  "password": password})
    return response

@pytest.mark.parametrize(
    ("study_id","title","description","password"),
    (("1","test_study_1_renamed","blupblup","test100"),
     ("1","","blupblup","test100"),
     ("1","test_study_1_renamed","","test100"),
     ("1","test_study_1_renamed","blupblup",""),
     ("1","","",""))
)

def test_modifiy_study(app,auth,client,study_id,title,description,password):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study_1","test","test")
    response = modifiy_study(client,study_id,title,description,password)
    assert response.status_code == 302

def test_modifiy_study_input_validation(app,auth,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study_1","test","test")
    create_study(client,"test_study_2","test2","test")
    response = modifiy_study(client,"2","test_study_1","test3","test")
    assert b"Titel already used for a different study. Please choose a different study title." in response.data


def delete_study(client,study_id):
    response = client.delete("/study/" + study_id)
    return response

def test_delete_study(app,auth,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study_1","test","test")
    with app.app_context():
        study = Study.query.filter_by(title="test_study_1").first()
        study_dir = study.get_image_dir()
        assert os.path.isdir(study_dir)

    response = delete_study(client,str(study.id))
    assert response.status_code == 200
    # test that the study was deleted drom the database
    with app.app_context():
        study = Study.query.filter_by(title="test_study_1").first()
        assert study is None
        assert not os.path.isdir(study_dir)

def create_design(client,study_id, json_data):
    response = client.post("/study/design/" + study_id, json=json_data)
    return response

tools_1 = {
    "test_tool":{
        "label":"test_label",
        "key_binding":"test_key",
        "status":"active"}
        }

scales_1 = [{"text":"test_scale_text","min":0,"max":3,"type":None}]


data_1 = {
    "instructions":"test_inst",
    "button_labels":"next_test",
    "text_color":"black",
    "background_color":"white",
    "numb_rois":-1,
    "numb_img":2,
    "numb_refimg":1,
    "transition_time":0,
    "show_viewport_info":True,
    "img_width":300,
    "img_height":300,
    "tools":tools_1,
    "scales":scales_1
}




def test_design(app,auth,client,study_id="1",json_data=data_1):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")
    response = create_design(client,study_id,json_data)
    assert response.status_code == 200


def create_imgset(client,study_id,json_data):
    response = client.post("/study/imgset/" + study_id, json=json_data)
    return response

stack_1 = {
    "div_id":"dicom_img_1",
    "name":"wad",
    "image_names":"sadasd",
    "viewport":"test_viewport",
    "tool_state":"test_tool_state"
}

imgset_1 = {"position":1,
            "stacks":[stack_1,stack_1]}

json_data_1 = {"imgset":imgset_1

}


imgset_2 = {"position":1,
            "stacks":[]}

json_data_2 = {"imgset":imgset_2
}

@pytest.mark.parametrize(
    ("study_id","position","json_data"),
    (("1","0",json_data_1),
     ("1","3",json_data_2))
)

def test_create_imgset(app,auth,client,study_id,position,json_data):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")    
    response = create_imgset(client,study_id, json_data)
    assert response.status_code == 200
    response = client.get("/study/imgset/" + study_id + "/" + position)
    assert response.status_code == 200

def update_imgset(client,study_id,position,json_data):
    response = client.put("/study/imgset/" + study_id + "/" + position, json=json_data)
    return response

@pytest.mark.parametrize(
    ("study_id","position","json_data"),
    (("1","0",json_data_1),)
)

def test_update_imgset(app,auth,client,study_id,position,json_data):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")    
    create_imgset(client,study_id, json_data)    
    
    response = update_imgset(client,study_id, position, json_data)
    assert response.status_code == 200


def delete_imgset(client,study_id,position):
    response = client.delete("/study/imgset/" + study_id + "/" + position)
    return response

@pytest.mark.parametrize(
    ("study_id","position"),
    (("1","0"),
     ("2","0"))
)

def test_delete_imgset(app,auth,client,study_id,position):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")    
    create_study(client,"test_study_2","Test","test")    

    create_imgset(client,study_id, json_data_1)
    response = delete_imgset(client,study_id, position)
    assert response.status_code == 200


def test_update_all_imgsets(app,auth,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")    
    response = client.put("/study/imgsets/1")
    assert response.status_code == 200


def test_delete_all_imgsets(app,auth,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","Test","test")    
    response = client.delete("/study/imgsets/1")
    assert response.status_code == 200


def test_study_create_file_upload(auth,app,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_4","file included","test")
    test_file_path = "/home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte Uli/HON/dicoms/"
    test_files_names = os.listdir(test_file_path)
    # upload dicoms
    test_files_dicoms = [file_name for file_name in test_files_names if ".dcm" in file_name][1:10]
    upload_file = [(open(os.path.join(test_file_path,test_files_name), 'rb'), test_files_name) for test_files_name in test_files_dicoms]
    upload_data = {"file":upload_file}    
    response = client.post('/files/1', data=upload_data)

    assert response.status_code == 200


def test_study_login(app,auth,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test description","test")
    auth.logout()
    auth.login("default_user","user")
    response = client.post("/study/login", data={"study_id":1,
                                                 "password":"test"
                                                }
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/study/run/1"


def test_study_login_input_validation(app,auth,client):
    # study not found
    auth.login("default_user","user")
    response = client.post("/study/login", data={"study_id":1,
                                                 "password":"test"
                                                }
    )
    assert response.status_code == 200
    assert b"Study not found." in response.data
    auth.logout()

    # study creation
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test description","test")
    auth.logout()

    # wrong password
    auth.login("default_user","user")
    response = client.post("/study/login", data={"study_id":1,
                                                 "password":"wrong password"
                                                }
    )
    assert response.status_code == 200
    assert b"Incorrect password." in response.data
    auth.logout()

def test_study_run(app,auth,client):
    # study creation
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test description","test")
    auth.logout()

    # access without study login
    auth.login("default_user","user")
    response = client.get("/study/run/1")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/study/login"

    # access successful but study empty
    auth.login("default_user","user")
    client.post("/study/login", data={"study_id":1, "password":"test"})
    response = client.get("/study/run/1")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/study/login"
    #assert b"Study is empty." in response.data

    # access successful but study already finihed

    # access successful



image_path_auto_test = "/home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte Uli/HON/Back-Ups PhantomX/images/Arthur/mass_1.05f"

@pytest.mark.parametrize(
    ("imgset_type","pos_pattern","neg_pattern"),
    (("standard",None,None),
     ("afc","pre","abs"))
)

@pytest.mark.parametrize(
    ("order"),
    (("ordered"),
     ("random"))
)

@pytest.mark.parametrize(
    ("stackmode"),
    (("single_images"),
     ("stacks"),
     ("test"))
)

@pytest.mark.parametrize(
    ("div_ids","div_ids_ref","viewport","viewport_ref","ref_stack_name"),
    ((["dicom_img_2"],[],"test",None,""),
     (["dicom_img_2","dicom_img_3"],[],"test",None,""),
     (["dicom_img_2","dicom_img_3"],["dicom_img_0"],"test","test","0001_pre_group1_2.dcm"),
     (["dicom_img_2","dicom_img_3"],["dicom_img_0"],"test","test","0001_pre_group1"))
)

def test_create_imgsets_auto(app,auth,client,imgset_type,order,stackmode,pos_pattern,neg_pattern,div_ids,div_ids_ref,viewport,viewport_ref,ref_stack_name):
    auth.login("default_study_admin","study_admin")
    # create study
    create_study(client,"test_1","file included","test")
    test_files_names = os.listdir(image_path_auto_test)
    # upload dicoms
    test_files_dicoms = [file_name for file_name in test_files_names if ".dcm" in file_name]
    upload_file = [(open(os.path.join(image_path_auto_test,test_files_name), 'rb'), test_files_name) for test_files_name in test_files_dicoms]
    upload_data = {"file":upload_file}    
    response = client.post('/files/1', data=upload_data) 
    assert response.status_code == 200

    # create study design (defaults)
    client.get("/study/design/1")

    # auto create study
    data_1 = {}
    data_1["study_id"] = 1
    data_1["imgset_type"] = imgset_type
    data_1["pos_pattern"] = pos_pattern
    data_1["neg_pattern"] = neg_pattern
    data_1["order"] = order
    data_1["stackmode"] = stackmode
    data_1["div_ids"] = div_ids
    data_1["div_ids_ref"] = div_ids_ref
    data_1["viewport"] = viewport
    data_1["viewport_ref"] = viewport_ref
    data_1["ref_stack_name"] = ref_stack_name
    response = client.post("/study/imgsets/auto",json=data_1)
    assert response.status_code == 200

    # login to study
    client.post("/study/login", data={"study_id":1, "password":"test"})
    response = client.get("/study/run/1")
    if ".dcm" in ref_stack_name and stackmode != "single_images" or ".dcm" not in ref_stack_name and stackmode == "single_images" and div_ids_ref:
        assert response.status_code == 302
    else:
        assert response.status_code == 200

        # study run vote
        stack_1 = {
        "div_id":"dicom_img_1",
        "name":"wad",
        "viewport":"test_viewport",
        "tool_state":"test_tool_state",
        "images":[]
        }
        
        
        data = {"scale_input":None,
                "picked_stack":stack_1
        }
        client.post('/vote/1/0', json=data)

        # check results
        client.get("/results/1/short")
        client.get("/results/1/full")



# missing get requests
urls = (("/study/modify/1",[2]),
        ("/study/design/1",[2]),
        ("/study/imgset/1/1",[1,2]),
        ("/study/imgsets/1",[2]),
        ("/study/files/1",[2]))

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
    (("default_user","user",1,"http://localhost/study/login"),
     ("default_study_admin","study_admin",2,"http://localhost/studies/overview"),
     ("default_user_admin","user_admin",3,"http://localhost/users/overview"))
)

def test_access_level_required(client,auth,url,access_level_required,username,password,access_level,redirect):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_4","file included","test")
    auth.logout()
    auth.login(username,password)
    response = client.get(url)
    if access_level in access_level_required:
        assert response.status_code == 200
    else:
        assert response.headers["Location"] == redirect