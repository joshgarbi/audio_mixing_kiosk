"""Password management module using bcrypt hashing and keyring storage."""
import getpass
import bcrypt
import keyring
from keyrings.alt.file import PlaintextKeyring

keyring.set_keyring(PlaintextKeyring())

def save_pass(user_id, pass_hash):
    """Store hashed password in keyring."""
    keyring.set_password("audio_mixing_kiosk", user_id, pass_hash.decode("utf-8"))

def new_pass(user_id, password):
    """Hash and store a new password."""
    salt = bcrypt.gensalt()
    pass_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    save_pass(user_id, pass_hash)

def verify_pass(user_id, password):
    """Verify a password against stored hash."""
    stored_hash = keyring.get_password("audio_mixing_kiosk", user_id)

    if not stored_hash:
        return False
    return bcrypt.checkpw(
        password.encode("utf-8"), stored_hash.encode("utf-8")
    )


if __name__ == "__main__":
    sys_password = getpass.getpass("Enter new password for admin: ")
    new_pass("admin", sys_password)
    print("Password set successfully.")
