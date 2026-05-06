"""Tests for configuration and validation functions."""
import json
import pytest
from uihelper import savedata, validate_ip, validate_port

def test_cfg_save():
    """Test saving configuration data to JSON."""
    label = "sample_label for testing"
    value = "*(6Gs?/.FLc"
    savedata(label, value)

    with open("src/cfg.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["TCP"][label] == value

    del data["TCP"][label]

    with open("src/cfg.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def test_ip_validation():
    """Test IP address validation function."""
    with open("src/cfg.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert validate_ip(None, "255.255.255.255", debug=True)
    assert validate_ip(None, "0.0.0.0", debug=True)
    assert not validate_ip(None, "256.100.0.0", debug=True)
    assert not validate_ip(None, "192.168.0", debug=True)
    assert not validate_ip(None, "-1.0.0.1", debug=True)
    assert not validate_ip(None, "192.r.0.1", debug=True)
    assert validate_ip(None, data["TCP"]["ip_address"], debug=True)

def test_port_validation():
    """Test port number validation function."""
    with open("src/cfg.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert validate_port(None, 0, debug=True)
    assert validate_port(None, "0", debug=True)
    assert validate_port(None, 65535, debug=True)
    assert not validate_port(None, 65536, debug=True)
    assert validate_port(None, data["TCP"]["port"], debug=True)
