
def test_metrics_endpoint(client):
    # Make a GET request to the metrics endpoint
    response = client.get("/metrics")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response content-type is correct for Prometheus metrics
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    # Check if the response contains the Prometheus metric key
    metrics_data = response.content.decode("utf-8")    
    assert "app_requests_total" in metrics_data