
def test_get_recipes(test_app, simple_test_data):
    recipe, ii, i = simple_test_data

    with test_app.test_client() as client:
        response = client.get("/recipes")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 1
        assert response.json[0] == recipe.dictionary

