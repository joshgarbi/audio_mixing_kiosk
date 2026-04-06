import pytest
import json
from uihelper import savedata, validate_ip, validate_port

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
        
    assert validate_ip(None, '255.255.255.255', debug=True) == True
    assert validate_ip(None, '0.0.0.0', debug=True) == True
    assert validate_ip(None, '256.100.0.0', debug=True) == False
    assert validate_ip(None, '192.168.0', debug=True) == False
    assert validate_ip(None, '-1.0.0.1', debug=True) == False
    assert validate_ip(None, '192.r.0.1', debug=True) == False
    assert validate_ip(None, data['TCP']["ip_address"], debug=True) == True
    
def test_port_validation():
    with open('src/cfg.json', 'r') as f:
        data = json.load(f)
        
    assert validate_port(None, 0, debug=True) == True
    assert validate_port(None, '0', debug=True) == True
    assert validate_port(None, 65535, debug=True) == True
    assert validate_port(None, 65536, debug=True) == False
    assert validate_port(None, data['TCP']['port'], debug=True) == True
    
