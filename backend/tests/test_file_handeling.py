import io
import os

from backend.flask_api.DBmodel import Study


def create_study(client, headers):
    response = client.post("/study", headers=headers)
    assert response.status_code == 200
    return response.get_json()["study"]


def test_upload_and_get_file(app, study_admin_headers, client):
    study = create_study(client, study_admin_headers)

    data = {
        "file": (io.BytesIO(b"test-data"), "stack_a.dcm"),
    }
    response = client.post(
        f"/upload_files/{study['id']}",
        data=data,
        headers={**study_admin_headers, "Origin": "http://localhost"},
    )
    assert response.status_code == 200

    response = client.get(
        f"/get_file/{study['user_id']}/{study['id']}/stack_a/stack_a.dcm",
        headers=study_admin_headers,
    )
    assert response.status_code == 200

    with app.app_context():
        study_db = Study.query.filter_by(id=study["id"]).first()
        assert os.path.isdir(study_db.get_image_dir())


def test_delete_files(study_admin_headers, client):
    study = create_study(client, study_admin_headers)

    data = {
        "file": (io.BytesIO(b"test-data"), "stack_b.dcm"),
    }
    response = client.post(
        f"/upload_files/{study['id']}",
        data=data,
        headers={**study_admin_headers, "Origin": "http://localhost"},
    )
    assert response.status_code == 200

    response = client.delete(
        f"/delete_files/{study['id']}",
        json=[{"name": "stack_b"}],
        headers={**study_admin_headers, "Origin": "http://localhost"},
    )
    assert response.status_code == 200
