import pytest


@pytest.mark.xfail(reason="/overlap uses calc_ious which is not implemented")
def test_overlap_endpoint(study_admin_headers, client):
    payload = {
        "tool_state": {
            "EllipticalRoi": {
                "uuid": "1",
                "handles": {"start": {"x": 0, "y": 0}, "end": {"x": 10, "y": 10}},
                "cachedStats": {"area": 1.0, "mean": 0.0, "stdDev": 0.0},
                "imageId": "test.dcm",
            }
        }
    }
    response = client.post("/overlap", json=payload, headers=study_admin_headers)
    assert response.status_code == 200
