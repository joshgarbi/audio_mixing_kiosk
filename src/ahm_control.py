"""AHM Control module for TCP communication with audio mixer device via MIDI protocol."""
import json
import socket
import time




# AHM_IP = "192.168.1.91"
# AHM_PORT = 51325

CHANNEL_OFFSET = 0x00
MUTE_NOTE = bytes([0x90, 0x00, 0x7F, 0x90, 0x00, 0x00])
UNMUTE_NOTE = bytes([0x90, 0x00, 0x3F, 0x90, 0x00, 0x00])
INCREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x7F])
DECREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x3F])
SYSEX_HEADER = bytes([0xF0, 0x00, 0x00, 0x1A, 0x50, 0x12, 0x01, 0x06])

with open('src/cfg.json', 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

AHM_IP = data["TCP"]["ip_address"]
AHM_PORT = data["TCP"]["port"]
# Persistent socket connection
_SOCKET = None

def initialize_connection():
    """Initialize TCP connection to AHM device."""
    global _SOCKET
    try:
        _SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _SOCKET.settimeout(1)
        _SOCKET.connect((AHM_IP, AHM_PORT))
        time.sleep(0.1)
        print("AHM connection established!")
        print(AHM_IP, AHM_PORT)
    except TimeoutError as e:
        print(AHM_IP, AHM_PORT)
        print(f"Failed to connect to AHM: {e}")
        _SOCKET = None

def close_connection():
    """Close TCP connection to AHM device."""
    if _SOCKET:
        try:
            _SOCKET.close()
            print("AHM connection closed.")
        except TimeoutError:
            pass

def test_connection():
    """Test AHM connection by sending a SYSEX query."""
    get_chname = SYSEX_HEADER + bytes([0x00, 0x09, 0x00, 0xF7])
    if _SOCKET:
        try:
            _SOCKET.sendall(get_chname)
            temp = _SOCKET.recv(4)
            return temp
        except TimeoutError:
            pass
    return None

def restart_connection():
    """Restart AHM connection after updating settings."""
    global _SOCKET
    update_settings()
    if _SOCKET:
        close_connection()
        _SOCKET = None
    initialize_connection()

def update_settings():
    """Update AHM IP and port from configuration file."""
    global AHM_IP
    global AHM_PORT
    with open('src/cfg.json', 'r', encoding='utf-8') as f:
        temp = json.load(f)

    AHM_IP = temp['TCP']['ip_address']
    AHM_PORT = temp['TCP']['port']

def mute():
    """Send mute command to all channels."""
    if _SOCKET:
        try:
            _SOCKET.sendall(MUTE_NOTE)
            time.sleep(0.1)
        except TimeoutError as e:
            print(f"Error: {e}")

def unmute():
    """Send unmute command to all channels."""
    if _SOCKET:
        try:
            _SOCKET.sendall(UNMUTE_NOTE)
            time.sleep(0.1)
        except TimeoutError as e:
            print(f"Error: {e}")

def set_ch_level(value, fader=0x00):
    """Set level for a specific channel (0-100 range)."""
    set_level = bytes([0xB0, 0x63, fader, 0xB0, 0x62, 0x17, 0xB0, 0x06])
    if _SOCKET:
        try:
            scaled_value = int(value * 127 / 100)
            level_byte = bytes([scaled_value])
            _SOCKET.sendall(set_level + level_byte)
        except TimeoutError as e:
            print(f'Error: {e}')

def get_ch_level(fader):
    """Get current level for a specific channel."""
    get_level = SYSEX_HEADER + bytes([0x00, 0x01, 0x0B, 0x17, fader, 0xF7])
    if _SOCKET:
        try:
            _SOCKET.sendall(get_level)
            temp = _SOCKET.recv(16)
            return temp[6] * 100 / 127
        except TimeoutError as e:
            print(f'Error: {e}')
            return -1
    return -1

def set_ch_gain(value, fader):
    set_level = bytes([0xB0, 0x63, fader, 0xB0, 0x62, 0x19, 0xB0, 0x06])
    if _SOCKET:
        try:
            scaled_value = int(value * 127 / 100) # Ensure 100 maps to 127, not 126
            level_byte = bytes([scaled_value])
            _SOCKET.sendall(set_level + level_byte)
            # time.sleep(0.1)
        except TimeoutError as e:
            print(f'Error: {e}')

def get_ch_gain(fader):
    get_level = SYSEX_HEADER + bytes([0x00, 0x01, 0x0B, 0x19, fader, 0xF7])
    if _SOCKET:
        try:
            _SOCKET.sendall(get_level)
            temp = _SOCKET.recv(16)
            return temp[6] * 100 / 127
        except TimeoutError as e:
            print(f'Error: {e}')
            return -1
    return -1


def get_ch_ppower(fader):
    get_ppower = SYSEX_HEADER + bytes([0x00, 0x01, 0x0B, 0x1B, fader, 0xF7])
    if _SOCKET:
        try:
            _SOCKET.sendall(get_ppower)
            temp = _SOCKET.recv(16)
            print(f"Phantom power status for fader {fader}: {temp[6]}")
            return temp[6]
        except TimeoutError as e:
            print(f'Error: {e}')
            return -1
    return -1

def toggle_ch_ppower(fader):
    ppower_off = bytes([0xB0, 0x63, fader, 0xB0, 0x62, 0x1B, 0xB0, 0x06, 0x00])
    ppower_on = bytes([0xB0, 0x63, fader, 0xB0, 0x62, 0x1B, 0xB0, 0x06, 0x7F])
    state = get_ch_ppower(fader)
    if _SOCKET:
        try:
            if state == 0x7F:
                _SOCKET.sendall(ppower_off)
            else:
                _SOCKET.sendall(ppower_on)
        except TimeoutError as e:
            print(f'Error: {e}')
