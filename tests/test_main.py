#!/usr/bin/python
import os

parent_directory = os.path.abspath('../src')


from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello World"}

def test_read_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"detail": "ok"}