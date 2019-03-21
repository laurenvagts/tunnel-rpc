import os
import tempfile

import pytest

from tunnel_rpc import server

@pytest.fixture
def client():
