import json
import os
import socket
import pytest
import time
from tools import within_margin
from ahm_control import test_connection, initialize_connection, close_connection, toggle_ch_ppower, get_ch_ppower, get_ch_gain, set_ch_gain, get_ch_level, set_ch_level

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
@pytest.mark.power
def test_phantom_power(pytestconfig):
    if pytestconfig.getoption("no_AHM"):
        pytest.skip("AHM control test skipped by command line option")
    initialize_connection()
    init_status = get_ch_ppower(0)
    toggle_ch_ppower(0)
    time.sleep(5)
    new_status = get_ch_ppower(0)
    assert init_status != new_status, "Phantom power state did not toggle"
    toggle_ch_ppower(0)
    time.sleep(5)
    final_status = get_ch_ppower(0)
    assert final_status == init_status, "Phantom power state did not return to original value"
    close_connection()
    
@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping AHM control test in CI environment",
)
@pytest.mark.power 
def test_gain_control(pytestconfig):
    if pytestconfig.getoption("no_AHM"):
        pytest.skip("AHM control test skipped by command line option")
    initialize_connection()
    init_gain = get_ch_gain(0)
    # assert init_gain == round((27 - 5) * 127 / 55), "Initial gain is not at expected value"
    new_gain = 90  # Set to max gain for testing
    time.sleep(1)
    set_ch_gain(new_gain, 0)
    time.sleep(5)
    updated_gain = get_ch_gain(0)
    time.sleep(1)
    assert within_margin(updated_gain, new_gain, 5), "Gain did not update correctly"
    set_ch_gain(init_gain, 0)  # Reset to original gain
    time.sleep(5)
    reset_gain = get_ch_gain(0)
    time.sleep(1)
    assert within_margin(reset_gain, init_gain, 5), "Gain did not reset to original value"
    close_connection()


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping AHM control test in CI environment",
)
@pytest.mark.power
def test_level_control(pytestconfig):
    if pytestconfig.getoption("no_AHM"):
        pytest.skip("AHM control test skipped by command line option")
    initialize_connection()
    init_level = get_ch_level(0)
    new_level = 80  # Set to a specific level for testing
    time.sleep(1)
    set_ch_level(new_level, 0)
    time.sleep(5)
    updated_level = get_ch_level(0)
    time.sleep(1)
    assert within_margin(updated_level, new_level, 5), "Level did not update correctly"
    set_ch_level(init_level, 0)  # Reset to original level
    time.sleep(5)
    reset_level = get_ch_level(0)
    time.sleep(1)
    assert within_margin(reset_level, init_level, 5), "Level did not reset to original value"
    close_connection()