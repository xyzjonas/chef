import pytest

from chef.controllers import RecipesController


@pytest.mark.asyncio
async def test_upload_thumb(simple_test_data, db_session, dummy_image):
    r, _, _, _ = simple_test_data

    assert not r.thumbnail_image

    await RecipesController().update_thumbnail(db_session, r.id, dummy_image)

    assert r.thumbnail_image


@pytest.mark.asyncio
async def test_upload_image(simple_test_data, db_session, dummy_image):
    r, _, _, _ = simple_test_data

    assert not r.detail_image
    assert not r.thumbnail_image

    await RecipesController().update_image(db_session, r.id, dummy_image)

    assert not r.thumbnail_image
    assert r.detail_image
