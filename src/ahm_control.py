### global socket refactor written by AI, 2024-06-20
import json
import socket
import time
from pythonping import ping




# AHM_IP = "192.168.1.91"
# AHM_PORT = 51325

channel = 0x00
MUTE_NOTE = bytes([0x90, 0x00, 0x7F, 0x90, 0x00, 0x00])
UNMUTE_NOTE = bytes([0x90, 0x00, 0x3F, 0x90, 0x00, 0x00])
INCREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x7F])
DECREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x3F])
SYSEX_HEADER = bytes([0xF0, 0x00, 0x00, 0x1A, 0x50, 0x12, 0x01, 0x06])

with open('src/cfg.json', 'r') as jsonfile:
    data = json.load(jsonfile)

AHM_IP = data["TCP"]["ip_address"]
AHM_PORT = data["TCP"]["port"]
# Persistent socket connection
_socket = None

def initialize_connection():

    global _socket
    try:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(1)
        _socket.connect((AHM_IP, AHM_PORT))
        time.sleep(0.1)
        print("AHM connection established!")
        print(AHM_IP, AHM_PORT)
    except Exception as e:
        print(AHM_IP, AHM_PORT)
        print(f"Failed to connect to AHM: {e}")
        _socket = None
        
def close_connection():
    if _socket:
        try:
            _socket.close()
            print("AHM connection closed.")
        except:
            return

def test_connection():
    GET_CHNAME = SYSEX_HEADER + bytes([0x00, 0x09, 0x00, 0xF7])
    if _socket:
        try:
            _socket.sendall(GET_CHNAME)
            data = _socket.recv(4)
            return data
        except:
            pass
    return None
    

def restart_connection():
    global _socket
    update_settings()
    if _socket:
        close_connection()
        _socket = None
    initialize_connection()
    
def update_settings():
    global AHM_IP
    global AHM_PORT
    with open('src/cfg.json', 'r') as f:
        data = json.load(f)

    AHM_IP = data['TCP']['ip_address']
    AHM_PORT = data['TCP']['port']
    
def mute():
    if _socket:
        try:
            _socket.sendall(MUTE_NOTE)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")

def unmute():
    if _socket:
        try:
            _socket.sendall(UNMUTE_NOTE)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")

def setCHlevel(value, fader=0x00):
    SETLEVEL = bytes([0xB0, 0x63, fader, 0xB0, 0x62, 0x17, 0xB0, 0x06]) 
    if _socket:
        try:
            scaled_value = int(value * 127 / 100) # Ensure 100 maps to 127, not 126
            level_byte = bytes([scaled_value])
            _socket.sendall(SETLEVEL + level_byte)
            # time.sleep(0.1)
        except Exception as e:
            print(f'Error: {e}')

def getCHlevel(fader):
    GETLEVEL = SYSEX_HEADER + bytes([0x00, 0x01, 0x0B, 0x17, fader, 0xF7])
    if _socket:
        try:
            _socket.sendall(GETLEVEL)
            data = _socket.recv(16)
            return data[6] * 100 / 127
        except Exception as e:
            print(f'Error: {e}')
            return -1
    return -1