def test_read_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() ==  { "status": "healthy"}