
# Test case for successful domain lookup
def test_lookup_valid_domain(client):
    response = client.get("/v1/tools/lookup?domain=example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["domain"] == "example.com"
    assert "ipv4" in data
    assert len(data["ipv4"]) > 0

# Test case for invalid domain lookup
def test_lookup_invalid_domain(client):
    response = client.get("/v1/tools/lookup?domain=invalid-domain")
    assert response.status_code == 400
    assert response.json() == {"detail": "Domain not found"}