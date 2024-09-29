"""
Test suite for verifying the Prometheus metrics exposed by the FastAPI
application.

This module contains a test case to ensure the following:
1. The /metrics endpoint returns the correct Prometheus metrics.
2. The endpoint returns a 200 status code, indicating successful
retrieval of the metrics.
3. The Content-Type of the response is correctly set to
"text/plain; charset=utf-8", the expected format for Prometheus metrics.
4. The response body includes the "app_requests_total" metric,
which tracks the number of requests made to the application.

The client fixture is used to interact with the FastAPI application,
sending HTTP requests to the /metrics endpoint and verifying the
responses.
"""


def test_metrics_endpoint(client):
    """
    Test case for the /metrics endpoint that exposes Prometheus metrics.

    This test ensures that:
    1. A GET request is made to the /metrics endpoint to
    retrieve Prometheus metrics.
    2. The request returns a 200 status code, indicating successful
    retrieval of the metrics.
    3. The Content-Type header in the response is "text/plain;
     charset=utf-8", which
     is the expected format for Prometheus metrics.
    4. The response body contains the specific Prometheus metric key,
    "app_requests_total",
    which is used to track the number of requests made to the application.

    Expected behavior:
    - Status code should be 200 (OK).
    - Content-Type should be "text/plain; charset=utf-8".
    - The "app_requests_total" metric should be present in the response.
    """
    # Make a GET request to the metrics endpoint
    response = client.get("/metrics")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response content-type is correct for Prometheus metrics
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    # Check if the response contains the Prometheus metric key
    metrics_data = response.content.decode("utf-8")
    assert "app_requests_total" in metrics_data
