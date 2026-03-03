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
    
