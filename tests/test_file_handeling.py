import os
import pytest
from test_study import create_study 

def upload_files(client,data,study_id):
    response = client.post('/files/' + study_id, data=data)
    return response

def delete_image_file(client,data,study_id):
    response = client.delete('/files/' + study_id, json=data)
    return response

def test_upload_image_file(auth,app,client):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test","test")

    test_file_path = "/home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte Uli/HON/dicoms/"
    test_files_names = os.listdir(test_file_path)
    # upload dicoms
    test_files_dicoms = [file_name for file_name in test_files_names if ".dcm" in file_name][1:10]
    upload_file = [(open(os.path.join(test_file_path,test_files_name), 'rb'), test_files_name) for test_files_name in test_files_dicoms]
    upload_data = {"file":upload_file}    
    response = upload_files(client,upload_data,"1")
    assert response.status_code == 200

    # upload zip
    test_files_zip = [file_name for file_name in test_files_names if ".zip" in file_name]
    upload_file = [(open(os.path.join(test_file_path,test_files_name), 'rb'), test_files_name) for test_files_name in test_files_zip]
    upload_data = {"file":upload_files}    
    response = upload_files(client,upload_data,"1")
    assert response.status_code == 200

    # empty upload
    response = upload_files(client,{},"1")
    assert response.status_code == 200

test_file_path = "/home/uli/Insync/uligenske@gmail.com/Google Drive/Projekte Uli/HON/dicoms/" 
test_files_names = os.listdir(test_file_path)
test_files_names = tuple((file_name) for file_name in test_files_names[1:10] if ".dcm" in file_name)

@pytest.mark.parametrize(
    ("filename"),
    test_files_names
    )
    
def test_get_dicom(auth,app,client,filename):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test","test")
    upload_file = (open(os.path.join(test_file_path,filename), 'rb'), filename)
    upload_data = {"file":upload_file}    
    upload_files(client,upload_data,"1")
    
    response = client.get('/get_file/2/1/' + filename)
    assert response.status_code == 200

    response = client.get('/get_file/2/1/1')
    assert response.status_code == 404

@pytest.mark.parametrize(
    ("filename"),
    test_files_names
    )

def test_delete_images(app,auth,client,filename):
    auth.login("default_study_admin","study_admin")
    create_study(client,"test_study","test","test")
    upload_file = (open(os.path.join(test_file_path,filename), 'rb'), filename)
    upload_data = {"file":upload_file}    
    upload_files(client,upload_data,"1")

    data = [filename]
    delete_image_file(client,data,"1") 