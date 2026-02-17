import socket
import time
import json

with open('src/cfg.json', 'r') as jsonfile:
    data = json.load(jsonfile)
ip_address = data['ip_address']
port = data['port']

# Example usage
def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set a timeout for the connection
            s.connect((ip_address, port))
            s.sendall(command.encode())
            print(f"Sent command: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")
        
