import ttkbootstrap as ttk
import tkinter as tk
from audiometer import GradientAudioMeter
from ttkbootstrap.constants import *
from fader import FaderManager
import json

def drawfaderbank(self, master):
    self.canvas = ttk.Canvas(master, width=self.width, height=self.height, highlightthickness=0)
    self.canvas.pack(fill="both", expand=True)
        
    self.faderBank = ttk.Frame(master, style="secondary.TFrame")
    self.faderBank.place(x=170, y=0, width=self.width - 170, height=self.height)
    
    # self.fader1 = Fader(self.faderBank, x=20, y=20, label="Fader 1")
    self.faders = FaderManager(self.faderBank)
    self.faders.createFaders()
    self.faders.updateAll()


def ip_settings(self, masterC):
    ip_frame = ttk.Frame(masterC)
    ip_frame.place(x=10, y=10, width=400, height=200)
    ipSettings = ttk.Entry(
        ip_frame,
        validate='focusout',
        validatecommand=lambda: validate_ip(ipSettings.get())          
    )

    ipSettings.delete(0, tk.END)
    ipSettings.insert(0, getdata('ip_address'))

    ipSettings.configure(font=36)
    ipSettings.place(x=5, y=5, width=200, height=50)
    
    portSettings = ttk.Entry(
        ip_frame,
        validate='focusout',
        validatecommand=lambda: validate_port(portSettings.get())
    )

    portSettings.delete(0, tk.END)
    portSettings.insert(0, getdata('port'))
    
    portSettings.configure(font=36)
    portSettings.place(x=210, y = 5, width=100, height=50)

def validate_port(port_str):
    try:
        port = int(port_str)
        if 0 <= port <= 65535:
            savedata('port', port)
        else:
            raise ValueError("Port number must be between 0 and 65535.")
    except:
        raise TypeError("Port Must be a number between 0 and 65535")

def validate_ip(ip_str):
    try:
        parts = ip_str.split('.')
        if len(parts) != 4:
            raise ValueError("IP address must have 4 parts.")
        for part in parts:
            num = int(part)
            if not (0 <= num <= 255):
                raise ValueError("Each part of IP must be between 0 and 255.")
        savedata('ip_address', ip_str)
    except:
        raise TypeError("Invalid IP address format. Must be in the form x.x.x.x where x is 0-255.")

def savedata(label, value):
    #read, modify, write to json config
    with open('src/cfg.json', 'r') as jsonfile:
        data = json.load(jsonfile)
   
    data[label] = value

    with open('src/cfg.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)      

def getdata(label):
    with open('src/cfg.json', 'r') as jsonfile:
        data = json.load(jsonfile)

    return data[label]