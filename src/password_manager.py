import keyring
import getpass

def save_pass(id, hash):
    keyring.set_password("audio_mixing_kiosk", id, hash.decode('utf-8'))

def new_pass(id, password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    save_pass(id, hash)
    
def verify_pass(id, password):
    stored_hash = keyring.get_password("audio_mixing_kiosk", id)
    if not stored_hash:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


if __name__ == "__main__":
    
    password = getpass.getpass("Enter new password for admin: ")
    new_pass("admin", password)
    print("Password set successfully.")