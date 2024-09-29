"""
Test suite setup for FastAPI application.

This module contains the setup needed for running test cases
on the FastAPI application.
It includes:
1. Adding the `src` directory to the system path for imports.
2. A pytest fixture to initialize and provide a `TestClient`
for interacting with the FastAPI application during tests.

This setup allows the test functions to send HTTP requests
to the application and assert the responses.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient
from main import app

# Add src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture(scope="module")
def client():
    """
    Fixture for setting up the FastAPI TestClient for testing.

    This fixture:
    - Initializes the FastAPI application using TestClient.
    - Yields the client instance for testing purposes.

    The `scope="module"` ensures that the same client instance
    is used for all tests within a module,
    reducing the overhead of creating a new client for every test.
    """

    with TestClient(app) as client:
        yield client
