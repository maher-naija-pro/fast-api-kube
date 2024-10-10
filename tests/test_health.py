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

    # Load the response data as JSON
    data = response.json()

    # Assert the main health status
    assert data["status"] == "healthy", "Main status is not healthy"

    # Check the timestamp is not None or empty
    assert data["timestamp"], "Timestamp is missing"

    # Check uptime is reported
    assert data["uptime"], "Uptime is missing"

    # Check the services array
    assert "services" in data, "Services data is missing"

    # Check service health details
    services = data["services"]
    assert services[0]["name"] == "database", "Service name is not 'database'"
    assert services[0]["status"] == "healthy", "Database service is not healthy"
    assert "latency" in services[0], "Latency data is missing"

    # Optionally, you could also check the type of latency to be float
    assert isinstance(services[0]["latency"], float), "Latency is not a float"
