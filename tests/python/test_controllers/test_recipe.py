from datetime import timedelta

import pytest

from chef.controllers import RecipesController, resolve_recipe_updated_at


@pytest.mark.asyncio
async def test_upload_image(simple_test_data, db_session, dummy_image):
    r, _, _, _ = simple_test_data

    assert not r.detail_image
    assert not r.thumbnail_image

    RecipesController().update_image(db_session, r.id, dummy_image)

    assert r.thumbnail_image
    assert r.detail_image


def test_resolve_recipe_updated_at_defaults_to_recipe_timestamp(simple_test_data):
    r, _, _, _ = simple_test_data
    assert resolve_recipe_updated_at(r) == r.updated_at


def test_resolve_recipe_updated_at_picks_latest_related_timestamp(db_session, simple_test_data):
    r, ii, i, t = simple_test_data

    future = r.updated_at + timedelta(days=1)
    i.updated_at = future
    db_session.add(i)
    db_session.commit()

    assert resolve_recipe_updated_at(r) == future
