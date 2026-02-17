### global socket refactor written by AI, 2024-06-20

import socket
import time
import atexit

AHM_IP = "192.168.1.91" 
PORT = 51325

MUTE_NOTE = bytes([0x90, 0x00, 0x7F, 0x90, 0x00, 0x00])
UNMUTE_NOTE = bytes([0x90, 0x00, 0x3F, 0x90, 0x00, 0x00])
INCREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x7F])  # CC#1 increment
DECREMENT = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x20, 0xB0, 0x06, 0x3F])  # CC#1 decrement
SETLEVEL = bytes([0xB0, 0x63, 0x00, 0xB0, 0x62, 0x17, 0xB0, 0x06])  # Base for setting level (append value byte)

# Persistent socket connection
_socket = None

def initialize_connection():
    """Initialize persistent socket connection on startup"""
    global _socket
    try:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(2)
        _socket.connect((AHM_IP, PORT))
        time.sleep(0.1)
        print("AHM connection established!")
    except Exception as e:
        print(f"Failed to connect to AHM: {e}")
        _socket = None

def close_connection():
    """Close persistent connection on shutdown"""
    global _socket
    if _socket:
        try:
            _socket.close()
            print("AHM connection closed")
        except:
            print("Error closing AHM connection")
            pass
        _socket = None

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

def setlevel(value):
    """Scale 0-100 to 0-127 and send to AHM"""
    if _socket:
        try:
            scaled_value = int(value * 127 / 100) # Ensure 100 maps to 127, not 126
            level_byte = bytes([scaled_value])
            _socket.sendall(SETLEVEL + level_byte)
            # time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
