# sample tests for project
import socket
import json
import os
import pytest
from src.uihelper import savedata, validate_ip, validate_port


def test_sample_function():
    assert 1 + 1 == 2
def test_another_sample_function():
    assert "hello".upper() == "HELLO"
def test_list_length():
    assert len([1, 2, 3]) == 3
    
@pytest.mark.skipif(
    os.environ.get('CI') == 'true',
    reason="Skipping AHM connection test in CI environment"
)

def test_ahm_connection():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a timeout for the connection
            with open('src/cfg.json', 'r') as jsonfile:
                data = json.load(jsonfile)
            ip = data["TCP"]['ip_address']
            port = data["TCP"]['port']
            s.connect((ip, port))  # Replace with actual IP and port
    except Exception as e:
        print(f"Connection failed: {e}")
        assert False, "Could not connect to AHM server"
    
def test_cfg_save():
    label = 'sample_label for testing'
    value = '*(6Gs?/.FLc'
    savedata(label, value)
    
    with open('src/cfg.json', 'r') as f:
        data = json.load(f)
        
    assert data['TCP'][label] == value
    
    del data['TCP'][label]
    
    with open('src/cfg.json', 'w') as f:
        json.dump(data, f, indent=4)
        
def test_ip_validation():
    with open('src/cfg.json', 'r') as f:
        data = json.load(f)
        
    assert validate_ip('255.255.255.255') == True
    assert validate_ip('0.0.0.0') == True
    assert validate_ip('256.100.0.0') == False
    assert validate_ip('192.168.0') == False
    assert validate_ip('-1.0.0.1') == False
    assert validate_ip('192.r.0.1') == False
    assert validate_ip(data['TCP']["ip_address"])
    
def test_port_validation():
    with open('src/cfg.json', 'r') as f:
        data = json.load(f)
        
    assert validate_port(0) == True
    assert validate_port('0') == True
    assert validate_port(65535) == True
    assert validate_port(65536) == False
    assert validate_port(data['TCP']['port'])
    
    
# run tests
if __name__ == "__main__":
    test_sample_function()
    test_another_sample_function()
    test_list_length()
    print("All tests passed!")