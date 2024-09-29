"""
Test suite for validating domain lookups in the FastAPI application.

This module contains test cases for the following scenarios:
1. Successfully looking up a valid domain name and receiving expected
   details, such as the domain name and associated IPv4 addresses.
2. Handling an invalid domain name lookup, ensuring the appropriate
   error status code and message are returned.

The client fixture is used to interact with the FastAPI application,
allowing the test cases to simulate HTTP requests to the relevant
endpoints and validate their responses.
"""


def test_lookup_valid_domain(client):
    """
    Test case for a successful domain lookup.

    This test ensures that:
    1. A GET request is made to the /v1/tools/lookup endpoint with a
     valid domain (example.com).
    2. The request returns a 200 status code, indicating a successful lookup.
    3. The response contains the domain name and at least one IPv4 address.

    Expected behavior:
    - Status code should be 200 (OK).
    - The domain name should be "example.com".
    - The response should include an "ipv4" field with at least one IP address.
    """
    response = client.get("/v1/tools/lookup?domain=example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["domain"] == "example.com"
    assert "ipv4" in data
    assert len(data["ipv4"]) > 0


# Test case for invalid domain lookup
def test_lookup_invalid_domain(client):
    """
    Test case for an invalid domain lookup.

    This test ensures that:
    1. A GET request is made to the /v1/tools/lookup endpoint with
     an invalid domain (invalid-domain).
    2. The request returns a 400 status code, indicating that the domain is not found.
    3. The response contains a specific error message.

    Expected behavior:
    - Status code should be 400 (Bad Request).
    - The response should contain the error message {"detail": "Domain not found"}.
    """
    response = client.get("/v1/tools/lookup?domain=invalid-domain")
    assert response.status_code == 400
    assert response.json() == {"detail": "Domain not found"}
