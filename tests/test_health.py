"""
Test suite for verifying the health status of the FastAPI application.

This module contains test cases to ensure the following:
1. The application exposes a /health endpoint that
indicates the service is running.
2. The /health endpoint returns the correct status code (200)
 and a JSON response that includes the application's health status.
3. These tests make use of FastAPI's TestClient to simulate HTTP
 requests and check the application's responses.

The client fixture is used to initialize the TestClient for testing.
"""


def test_read_health_check(client):
    """
    Test case for the /health endpoint to verify
     the application's health status.

    This test ensures that:
    1. A GET request is made to the /health endpoint.
    2. The endpoint returns a 200 status code, indicating
     that the service is up
    3. The JSON response contains the expected status message,
     confirming that the application is healthy.

    Expected behavior:
    - The response status code should be 200.
    - The JSON response should be {"status": "healthy"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
