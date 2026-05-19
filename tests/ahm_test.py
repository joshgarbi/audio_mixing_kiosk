import json
import os
import socket
import pytest
from ahm_control import test_connection, toggle_ch_ppower, get_ch_ppower


_connect_status = False

@pytest.fixture
def get_test_connection():
    """Get test connection result."""
    return test_connection()

@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping AHM connection test in CI environment",
)
def test_l_ahm_connection(pytestconfig):
    """Test AHM TCP connection."""
    if pytestconfig.getoption("no_AHM"):
        pytest.skip("AHM connection test skipped by command line option")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a timeout for the connection
            with open("src/cfg.json", "r", encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)
            ip = data["TCP"]["ip_address"]
            port = data["TCP"]["port"]
            s.connect((ip, port))
            _connect_status = True
    except TimeoutError as e:
        print(f"Connection failed: {e}")
        assert False, "Could not connect to AHM server"

@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping AHM control test in CI environment",
)
def test_phantom_power(pytestconfig):
    if pytestconfig.getoption("no_AHM"):
        pytest.skip("AHM control test skipped by command line option")
    init_status = get_ch_ppower()
    toggle_ch_ppower()
    new_status = get_ch_ppower()
    assert init_status != new_status, "Phantom power state did not toggle"
    toggle_ch_ppower()  # Toggle back to original state
    final_status = get_ch_ppower()
    assert final_status == init_status, "Phantom power state did not return to original value"
    