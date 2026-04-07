import pytest
from password_manager import new_pass, verify_pass

def test_password_hashing_and_verification():
    password = "my_secure_password"
    new_pass("test_user", password)
    assert verify_pass("test_user", password) == True
    assert verify_pass("test_user", "wrong_password") == False
    
    
    
    
