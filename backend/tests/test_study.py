import os

import pytest

from backend.flask_api.DBmodel import Image, Stack, Study, db


def create_study(client, headers):
    response = client.post("/study", headers=headers)
    assert response.status_code == 200
    return response.get_json()["study"]


def create_stack(app, study_id, user_id, name="stack_a", image_name="image_a.dcm"):
    with app.app_context():
        base_url = f"http://localhost/flask-api/get_file/{user_id}/{study_id}/{name}/"
        stack = Stack(study_id=study_id, base_url=base_url, name=name)
        image = Image(name=image_name)
        stack.images.append(image)
        db.session.add(stack)
        db.session.commit()
        return stack


def build_stack_payload(stack_id, name, div_id="dicom_img_0"):
    return {
        "stack_id": stack_id,
        "div_id": div_id,
        "name": name,
        "viewport": {
            "scale": 1,
            "translation": {"x": 0, "y": 0},
            "voi": {"windowWidth": 100, "windowCenter": 50},
            "rotation": 0,
        },
        "tool_state": [],
        "segmentation_data": None,
    }


def test_create_and_list_studies(app, study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    assert study["id"]

    response = client.get("/studies", headers=study_admin_headers)
    assert response.status_code == 200
    assert response.get_json()["studies"]

    with app.app_context():
        study_db = Study.query.filter_by(id=study["id"]).first()
        assert study_db is not None
        assert os.path.isdir(study_db.get_image_dir())


def test_update_study(study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    response = client.put(
        f"/study/{study['id']}",
        json={
            "title": "updated title",
            "password": "new-pass",
            "description": "new description",
        },
        headers=study_admin_headers,
    )
    assert response.status_code == 200


def test_get_study_owner(study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    response = client.get(f"/study/{study['id']}", headers=study_admin_headers)
    assert response.status_code == 200
    assert response.get_json()["study"]["id"] == study["id"]


def test_study_login_and_get_study_participant(
    participant_headers, study_admin_headers, client
):
    study = create_study(client, study_admin_headers)

    response = client.post(
        "/study/login",
        json={"study_id": study["id"], "password": ""},
        headers=participant_headers,
    )
    assert response.status_code == 201
    participant_token = response.get_json()["accessToken"]
    study_headers = {"Authorization": f"Bearer {participant_token}"}

    response = client.get(f"/study/{study['id']}", headers=study_headers)
    assert response.status_code == 200


def test_design_update(study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    response = client.put(
        f"/study/design/{study['id']}",
        json={
            "instructions": "do the thing",
            "button_labels": "Next",
            "text_color": "black",
            "background_color": "white",
            "numb_img": 1,
            "numb_refimg": 0,
            "transition_time": 0,
            "show_viewport_info": True,
            "img_height": 512,
            "img_height_auto": True,
            "img_per_row": 1,
            "numb_rois": 0,
            "tools": [
                {
                    "cs_name": "Length",
                    "key_binding": "l",
                    "settings": {"mouseButtonMask": 1},
                }
            ],
            "scales": [
                {
                    "text": "quality",
                    "min": 1,
                    "max": 5,
                    "type": "likert",
                    "labels": [1, 2, 3, 4, 5],
                }
            ],
        },
        headers=study_admin_headers,
    )
    assert response.status_code == 200


def test_imgset_crud(app, study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    stack = create_stack(app, study["id"], study["user_id"], name="stack_a")

    payload = {
        "position": 0,
        "stacks": [build_stack_payload(stack.id, stack.name)],
    }
    response = client.post(
        f"/study/imgset/{study['id']}", json=payload, headers=study_admin_headers
    )
    assert response.status_code == 200

    response = client.get(
        f"/study/imgset/{study['id']}/0", headers=study_admin_headers
    )
    assert response.status_code == 200

    response = client.put(
        f"/study/imgset/{study['id']}/0",
        json=payload,
        headers=study_admin_headers,
    )
    assert response.status_code == 200

    response = client.delete(
        f"/study/imgset/{study['id']}/0", headers=study_admin_headers
    )
    assert response.status_code == 200


def test_imgsets_bulk_update_and_delete(app, study_admin_headers, client):
    study = create_study(client, study_admin_headers)
    stack = create_stack(app, study["id"], study["user_id"], name="stack_a")

    payload = [
        {
            "position": 0,
            "stacks": [build_stack_payload(stack.id, stack.name)],
        }
    ]
    response = client.post(
        f"/study/imgsets/{study['id']}", json=payload, headers=study_admin_headers
    )
    assert response.status_code == 200

    response = client.put(
        f"/study/imgsets/{study['id']}",
        json={
            "scale": 1.5,
            "posX": 5,
            "posY": 10,
            "windowWidth": 120,
            "windowCenter": 60,
            "rotation": 0,
        },
        headers=study_admin_headers,
    )
    assert response.status_code == 200

    response = client.delete(
        f"/study/imgsets/{study['id']}", headers=study_admin_headers
    )
    assert response.status_code == 200
