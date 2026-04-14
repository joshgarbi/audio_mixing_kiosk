import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
import json
from fader import FaderManager
from ahm_control import test_connection, restart_connection
from password_manager import verify_pass



def drawfaderbank(self, masterC):
    self.canvas = ttk.Canvas(masterC, width=self.width, height=self.height, highlightthickness=0)
    self.canvas.pack(fill="both", expand=True)
        
    self.faderBank = ttk.Frame(masterC, style="secondary.TFrame")
    self.faderBank.place(x=170, y=0, width=self.width - 170, height=self.height)
    
    # self.fader1 = Fader(self.faderBank, x=20, y=20, label="Fader 1")
    self.faders = FaderManager(self.faderBank)
    self.faders.createFaders()
    self.faders.updateAll()


def ip_settings(self, masterC):
    self.masterC = masterC
    style = ttk.Style()

    style.configure("Red.TLabel", foreground="red")
    style.configure("Green.TLabel", foreground="green")

    ip_frame = ttk.Frame(masterC)
    ip_frame.place(x=10, y=10, width=400, height=200)

    vip_cmd = (ip_frame.register(lambda p: validate_ip(self, p)), '%P')
    vport_cmd = (ip_frame.register(lambda p: validate_port(self, p)), '%P')

    ipSettings = ttk.Entry(
        ip_frame,
        validate='focusout',
        validatecommand=vip_cmd,
        
    )

    ipSettings.delete(0, tk.END)
    ipSettings.insert(0, getdata('ip_address'))

    ipSettings.configure(font=36)
    ipSettings.place(x=5, y=5, width=200, height=50)
    
    portSettings = ttk.Entry(
        ip_frame,
        validate='focusout',
        validatecommand=vport_cmd,
    )

    portSettings.delete(0, tk.END)
    portSettings.insert(0, getdata('port'))
    
    portSettings.configure(font=36)
    portSettings.place(x=210, y = 5, width=100, height=50)
    
    self.connectionStatus = ttk.Label(
        ip_frame,
        text="STATUS",
    )
    self.connectionStatus.configure(font=36)
    self.connectionStatus.place(x=315, y=5, width=80, height=50)

    if test_connection() != None:
        self.connectionStatus.configure(style="Green.TLabel")
    else:
        self.connectionStatus.configure(style="Red.TLabel")
        
def handle_reconnection(self):
    self.connectionStatus.configure(style="Red.TLabel")
    restart_connection()
    
    if test_connection() is not None:
        self.connectionStatus.configure(style="Green.TLabel")

    else:
        self.connectionStatus.configure(style="Red.TLabel")



def validate_port(self, port_str, debug=False):
    try:
        port = int(port_str)
        if 0 <= port <= 65535:
            savedata('port', port)
            if not debug:
                handle_reconnection(self)
            return True
    except:
        pass    
    return False

def validate_ip(self, ip_str, debug=False):
    try:
        parts = ip_str.split('.')
        if len(parts) != 4:
            raise ValueError("IP address must have 4 parts.")
        for part in parts:
            num = int(part)
            if not (0 <= num <= 255):
                raise ValueError("Each part of IP must be between 0 and 255.")
        savedata('ip_address', ip_str)
        if not debug:
            handle_reconnection(self)
        return True
    except:
        return False



def savedata(label, value):
    #read, modify, write to json config
    with open('src/cfg.json', 'r') as jsonfile:
        data = json.load(jsonfile)
   
    data["TCP"][label] = value

    with open('src/cfg.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)      

def getdata(label):
    with open('src/cfg.json', 'r') as jsonfile:
        data = json.load(jsonfile)

    return data["TCP"][label]

def prompt_password(self, MasterC):
    # Instead of Toplevel, create a Frame on top of the existing MasterC
    self.password_overlay = ttk.Frame(MasterC, style="Dark.TFrame")
    
    # Place it to cover the entire screen (assuming MasterC is your root/main container)
    self.password_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # Create a centered container inside the overlay for the actual "dialog" look
    dialog_frame = ttk.Frame(self.password_overlay, padding=40, bootstyle="secondary")
    dialog_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=400)

    label = ttk.Label(dialog_frame, text="Enter Password", font=("Arial", 18))
    label.pack(pady=20)
    
    self.password_entry = ttk.Entry(dialog_frame, show="*", font=("Arial", 16))
    self.password_entry.pack(pady=10)
    self.password_entry.focus_set()
    
    submit_button = ttk.Button(dialog_frame, text="Submit", width=16, bootstyle="primary", style="Dialog.TButton", command=lambda: check_password(self=self))
    submit_button.pack(side="left", padx=60, pady=20)

    cancel_button = ttk.Button(dialog_frame, text="Cancel", width=16, bootstyle="secondary", style="Dialog.TButton", command=self.password_overlay.destroy)
    cancel_button.pack(side="right", padx=60, pady=20)

def check_password(self):
    password = self.password_entry.get()
    if verify_pass("admin", password):
        print("Password correct")
        self.password_overlay.destroy()
        self.openSettings()
    else:
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(style="Red.TEntry")
        
    
    
