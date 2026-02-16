# sample tests for project
import socket
import json
import os
import pytest


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
            ip = data['ip_address']
            port = data['port']
            s.connect(('localhost', port))  # Replace with actual IP and port
    except Exception as e:
        print(f"Connection failed: {e}")
        assert False, "Could not connect to AHM server"
    
    
# run tests
if __name__ == "__main__":
    test_sample_function()
    test_another_sample_function()
    test_list_length()
    print("All tests passed!")