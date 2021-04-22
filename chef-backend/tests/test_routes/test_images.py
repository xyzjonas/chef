import os
import pytest


@pytest.fixture()
def image(test_image):
    with open(test_image, "rb") as img:
        yield img


def test_upload(test_app, simple_test_data, image):
    r, ii, i, t = simple_test_data
    with test_app.test_client() as client:
        data = {"image": (image, "test_image.jpg")}
        res = client.post(f"/recipes/{r.id}/image", content_type='multipart/form-data', data=data)
        assert res.status_code == 200


def test_upload_category(test_app, category_with_tag, image):
    c, t = category_with_tag
    with test_app.test_client() as client:
        data = {"image": (image, "test_image.jpg")}
        res = client.post(f"/categories/{c.id}/image", content_type='multipart/form-data', data=data)
        assert res.status_code == 200
