import os
import keyring
from password_manager import new_pass, verify_pass

# Check if running in a CI environment
if os.getenv("CI"):
    from keyrings.alt.file import PlaintextKeyring
    keyring.set_keyring(PlaintextKeyring())

def test_password_hashing_and_verification():
    """Test password hashing and verification functions."""
    password = "my_secure_password"
    new_pass("test_user", password)
    assert verify_pass("test_user", password)
    assert not verify_pass("test_user", "wrong_password")
