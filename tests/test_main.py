#!/usr/bin/python
import os


import sys
# Add src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root_in_kubernetes_env(monkeypatch):
    # Simulate being in a Kubernetes environment
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "localhost")
    response = client.get("/")
    
    assert response.status_code == 200
    json_data = response.json()
    
    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is True
    assert isinstance(json_data["date"], int)

def test_root_not_in_kubernetes_env(monkeypatch):
    # Simulate not being in a Kubernetes environment
    monkeypatch.delenv("KUBERNETES_SERVICE_HOST", raising=False)
    response = client.get("/")
    
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is False
    assert isinstance(json_data["date"], int)


def test_read_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() ==  { "status": "healthy"}

def test_validate_ip_valid_ipv4():
    response = client.post("/v1/tools/validate", json={"ip": "192.168.1.1"})
    assert response.status_code == 200
    assert response.json() == {"ip": "192.168.1.1", "valid": True}

def test_validate_ip_invalid_ip():
    response = client.post("/v1/tools/validate", json={"ip": "999.999.999.999"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid IP address"}

def test_validate_ip_valid_ipv6():
    response = client.post("/v1/tools/validate", json={"ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"})
    assert response.status_code == 200
    assert response.json() == {"ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334", "valid": False}

def test_metrics_endpoint():
    # Make a GET request to the metrics endpoint
    response = client.get("/metrics")
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the response content-type is correct for Prometheus metrics
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    # Check if the response contains the Prometheus metric key
    metrics_data = response.content.decode("utf-8")    
    assert "app_requests_total" in metrics_data

