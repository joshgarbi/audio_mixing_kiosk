import pytest
import socket
import os
import json
from ahm_control import initialize_connection, close_connection, getCHlevel, test_connection

_connect_status = False

@pytest.fixture
def get_test_connection():
    return test_connection()

@pytest.mark.skipif(
    os.environ.get('CI') == 'true',
    reason="Skipping AHM connection test in CI environment"
)

def testL_ahm_connection():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a timeout for the connection
            with open('src/cfg.json', 'r') as jsonfile:
                data = json.load(jsonfile)
            ip = data["TCP"]['ip_address']
            port = data["TCP"]['port']
            s.connect((ip, port))
            _connect_status = True
    except Exception as e:
        print(f"Connection failed: {e}")
        assert False, "Could not connect to AHM server"
        
# @pytest.mark.skipif(
#     _connect_status == False, 
#     reason="Console not connected, skipping test"
# )
def test_ahm_connection(get_test_connection):
    assert get_test_connection

    