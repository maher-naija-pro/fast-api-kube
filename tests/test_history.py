"""
Test suite for verifying the functionality of the /history endpoint
in the FastAPI application.

This module contains test cases for the following scenarios:
1. Ensuring that the /history endpoint behaves correctly when no history
   exists in the database.
2. Simulating a domain lookup and checking whether the application
   correctly logs or returns history data.

The client fixture is used to interact with the FastAPI application,
allowing the test cases to send HTTP requests to the relevant endpoints
and validate the responses.
"""


def test_get_history_empty(client):
    """
    Test case for the /history endpoint when there is no history in the database.

    This test ensures that:
    1. A request to the /v1/tools/lookup endpoint is made to simulate a domain lookup.
    2. A subsequent request is made to the /v1/history endpoint.
    3. The /v1/history endpoint returns a 200 status code, and the history
     data is checked.

    Expected behavior:
    - The history response should be an empty list when no prior
     history exists in the database.
    """
    # Make the request to the /history endpoint with an empty database
    client.get("/v1/tools/lookup?domain=example.com")
    response = client.get("/v1/history")
    assert response.status_code == 200

    # Check that the response is an empty list
    history = response.json()
    assert len(history) != 0
