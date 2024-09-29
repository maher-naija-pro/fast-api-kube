# Test case for /history when there's no history in the database
def test_get_history_empty(client):
    # Make the request to the /history endpoint with an empty database
    response = client.get("/v1/history")
    assert response.status_code == 200

    # Check that the response is an empty list
    history = response.json()
    assert len(history) != 0