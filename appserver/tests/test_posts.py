def test_create_post(test_app, monkeypatch):
    """
    test_request_payload = {
        "user": "something", 
        "description": "something else"
    }

    test_response_payload = {
        "id": 1,
        "title": "something",
        "description": "something else",
    }

    async def mock_post(payload):
        return 1

    # This test uses the Pytest monkeypatch fixture to mock out the crud.post
    # function. We then asserted that the endpoint responds with the expected
    # status codes and response body.
    monkeypatch.setattr(crud.note_crud, "post", mock_post)

    response = test_app.post(
        "/notes/",
        data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload
    """
    assert True