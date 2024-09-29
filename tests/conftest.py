#!/usr/bin/python
#!/usr/bin/python
import os


import sys
# Add src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    """Fixture for setting up the TestClient."""
    with TestClient(app) as client:
        yield client
