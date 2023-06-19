import os

import pytest


@pytest.fixture()
def image(dummy_image):
    with open(dummy_image, "rb") as img:
        yield img


def test_upload(http_client, simple_test_data, image):
    r, ii, i, t = simple_test_data
    # with open(fpath, "wb") as f:
    #     response = client.post("/", files={"file": ("filename", f, "image/jpeg")})
    data = {"image": ("test_image.jpg", image, "image/jpeg")}
    res = http_client.post(f"/api/images/recipes/{r.id}", files=data)
    assert res.status_code == 200


def test_upload_category(http_client, category_with_tag, image):
    c, t = category_with_tag
    data = {"image": ("test_image.jpg", image, "image/jpeg")}
    res = http_client.post(f"/api/images/categories/{c.id}", files=data)
    assert res.status_code == 200
