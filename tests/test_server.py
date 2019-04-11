import os
import tempfile

import pytest

from tunnel_rpc import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    yield client
