def test_validate_ip_valid_ipv4(client):
    response = client.post("/v1/tools/validate", json={"ip": "192.168.1.1"})
    assert response.status_code == 200
    assert response.json() == {"ip": "192.168.1.1", "valid": True}

def test_validate_ip_invalid_ip(client):
    response = client.post("/v1/tools/validate", json={"ip": "999.999.999.999"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid IP address"}

def test_validate_ip_valid_ipv6(client):
    response = client.post("/v1/tools/validate", json={"ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"})
    assert response.status_code == 200
    assert response.json() == {"ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334", "valid": False}