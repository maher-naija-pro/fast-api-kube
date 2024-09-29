"""
Test suite for validating IP addresses via the /v1/tools/validate endpoint
in the FastAPI application.

This module contains test cases for the following scenarios:
1. Validating a valid IPv4 address and ensuring the response confirms
   that the IP is valid.
2. Validating an invalid IP address and ensuring the appropriate error
   message and status code are returned.
3. Validating a valid IPv6 address, with the expectation that it
   might return a "valid" flag based on the application’s business logic.

The client fixture is used to interact with the FastAPI application,
allowing the test cases to simulate HTTP requests and validate
responses.
"""


def test_validate_ip_valid_ipv4(client):
    """
    Test case for validating a valid IPv4 address.

    This test ensures that:
    1. A POST request is made to the /v1/tools/validate endpoint
    with a valid IPv4 address.
    2. The request returns a 200 status code, indicating successful
    validation.
    3. The response JSON contains the correct IP address and a "valid"
    flag set to True.

    Expected behavior:
    - Status code should be 200 (OK).
    - The response should confirm the IP is valid with the correct
    IP address
    and "valid" flag set to True.
    """
    response = client.post("/v1/tools/validate", json={"ip": "192.168.1.1"})
    assert response.status_code == 200
    assert response.json() == {"ip": "192.168.1.1", "valid": True}


def test_validate_ip_invalid_ip(client):
    """
    Test case for validating an invalid IP address.

    This test ensures that:
    1. A POST request is made to the /v1/tools/validate endpoint
     with an invalid IP address.
    2. The request returns a 400 status code, indicating
    a validation failure.
    3. The response contains a specific error message indicating
    that the IP address is invalid.

    Expected behavior:
    - Status code should be 400 (Bad Request).
    - The response should include the error message
    {"detail": "Invalid IP address"}.
    """
    response = client.post("/v1/tools/validate", json={"ip": "999.999.999.999"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid IP address"}


def test_validate_ip_valid_ipv6(client):
    """
    Test case for validating a valid IPv6 address.

    This test ensures that:
    1. A POST request is made to the /v1/tools/validate endpoint
    with a valid IPv6 address.
    2. The request returns a 200 status code, indicating successful
    validation.
    3. The response contains the correct IP address, but the
    "valid" flag is set to False,
    based on business logic.

    Expected behavior:
    - Status code should be 200 (OK).
    - The response should confirm the IP address with the correct IP address and
     "valid" flag set according to business logic.
    """
    response = client.post(
        "/v1/tools/validate", json={"ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "valid": False,
    }
