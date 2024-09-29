"""
Test suite for verifying the behavior of the root ("/") endpoint in
various environments (Kubernetes and non-Kubernetes) for the FastAPI
application.

This module contains test cases for the following scenarios:
1. Simulating the application running inside a Kubernetes environment
   by setting the `KUBERNETES_SERVICE_HOST` environment variable.
2. Simulating the application running outside of a Kubernetes
   environment by removing the `KUBERNETES_SERVICE_HOST` variable.
3. Verifying that the correct version, Kubernetes flag, and timestamp
   are returned by the root ("/") endpoint in both cases.

The client fixture is used to interact with the FastAPI application,
allowing the test cases to simulate HTTP requests and validate
responses.
"""


def test_root_in_kubernetes_env(client, monkeypatch):
    """
    Test case for the root ("/") endpoint when the application
    is running in a Kubernetes environment.

    This test ensures that:
    1. The environment is simulated as a Kubernetes environment
     by setting the `KUBERNETES_SERVICE_HOST` environment variable.
    2. A GET request is made to the root ("/") endpoint.
    3. The response status code is 200, indicating
    successful access to the root endpoint.
    4. The JSON response contains the correct application version,
    a flag indicating the application is in a Kubernetes environment,
    and a valid date in integer format (likely a timestamp).

    Expected behavior:
    - Status code should be 200 (OK).
    - The `version` field in the response should be "0.1.0".
    - The `kubernetes` field should be `True` since the application
    is simulated to be in a Kubernetes environment.
    - The `date` field should be an integer (timestamp).
    """

    # Simulate being in a Kubernetes environment
    monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "localhost")
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is True
    assert isinstance(json_data["date"], int)


def test_root_not_in_kubernetes_env(client, monkeypatch):
    """
    Test case for the root ("/") endpoint when the application is not running
     in a Kubernetes environment.

    This test ensures that:
    1. The environment is simulated as not being a Kubernetes environment by removing
    the `KUBERNETES_SERVICE_HOST` environment variable.
    2. A GET request is made to the root ("/") endpoint.
    3. The response status code is 200, indicating
    successful access to the root endpoint.
    4. The JSON response contains the correct application version, a flag indicating the
     application is not in a Kubernetes environment,
       and a valid date in integer format (likely a timestamp).

    Expected behavior:
    - Status code should be 200 (OK).
    - The `version` field in the response should be "0.1.0".
    - The `kubernetes` field should be `False` since the application is simulated to
    be outside of a Kubernetes environment.
    - The `date` field should be an integer (timestamp).
    """
    monkeypatch.delenv("KUBERNETES_SERVICE_HOST", raising=False)
    response = client.get("/")

    assert response.status_code == 200
    json_data = response.json()

    assert json_data["version"] == "0.1.0"
    assert json_data["kubernetes"] is False
    assert isinstance(json_data["date"], int)
