

def test_root_in_kubernetes_env(client,monkeypatch):
    # Simulate being in a Kubernetes environment
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "localhost")
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is True
    assert isinstance(json_data["date"], int)

def test_root_not_in_kubernetes_env(client,monkeypatch):
    # Simulate not being in a Kubernetes environment
    monkeypatch.delenv("KUBERNETES_SERVICE_HOST", raising=False)
    response = client.get("/")
    
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is False
    assert isinstance(json_data["date"], int)