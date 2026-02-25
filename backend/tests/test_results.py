from backend.flask_api.DBmodel import Image, Stack, db


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


def test_save_and_delete_result(app, client, study_admin_headers, participant_headers):
    study = create_study(client, study_admin_headers)
    stack = create_stack(app, study["id"], study["user_id"], name="stack_a")

    response = client.post(
        f"/study/imgset/{study['id']}",
        json={"position": 0, "stacks": [build_stack_payload(stack.id, stack.name)]},
        headers=study_admin_headers,
    )
    assert response.status_code == 200
    imgset_id = response.get_json()["imgset"]["id"]

    response = client.post(
        "/study/login",
        json={"study_id": study["id"], "password": ""},
        headers=participant_headers,
    )
    participant_token = response.get_json()["accessToken"]
    study_headers = {"Authorization": f"Bearer {participant_token}"}

    response = client.post(
        f"/study/result/{study['id']}",
        json={
            "imgset_id": imgset_id,
            "scale_input": None,
            "picked_stack": build_stack_payload(stack.id, stack.name),
        },
        headers=study_headers,
    )
    assert response.status_code == 200
    assert response.get_json()["result"]["imgset_id"] == imgset_id

    response = client.delete(
        f"/result/{study['id']}/1", headers=study_admin_headers
    )
    assert response.status_code == 200


def test_results_csv_roundtrip(app, client, study_admin_headers, participant_headers):
    study = create_study(client, study_admin_headers)
    stack = create_stack(app, study["id"], study["user_id"], name="stack_a")

    response = client.post(
        f"/study/imgset/{study['id']}",
        json={"position": 0, "stacks": [build_stack_payload(stack.id, stack.name)]},
        headers=study_admin_headers,
    )
    imgset_id = response.get_json()["imgset"]["id"]

    response = client.post(
        "/study/login",
        json={"study_id": study["id"], "password": ""},
        headers=participant_headers,
    )
    participant_token = response.get_json()["accessToken"]
    study_headers = {"Authorization": f"Bearer {participant_token}"}

    client.post(
        f"/study/result/{study['id']}",
        json={
            "imgset_id": imgset_id,
            "scale_input": None,
            "picked_stack": build_stack_payload(stack.id, stack.name),
        },
        headers=study_headers,
    )

    response = client.get(f"/results/{study['id']}", headers=study_admin_headers)
    assert response.status_code == 200

    response = client.get(f"/results/{study['id']}/download")
    assert response.status_code == 200
