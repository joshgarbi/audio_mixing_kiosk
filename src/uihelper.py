"""UI helper utilities for settings, validation, and password prompts."""
import json
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, RIGHT
from fader import FaderManager
from ahm_control import test_connection, restart_connection
from password_manager import verify_pass



def drawfaderbank(self, master_c):
    """Draw the fader bank widget."""
    self.canvas = ttk.Canvas(
        master_c,
        width=self.width,
        height=self.height,
        highlightthickness=0,
    )
    self.canvas.pack(fill="both", expand=True)

    self.faderBank = ttk.Frame(master_c, style="secondary.TFrame")
    self.faderBank.place(
        x=170, y=0, width=self.width - 170, height=self.height
    )

    self.faders = FaderManager(self.faderBank)
    self.faders.create_faders()
    self.faders.update_all()


def ip_settings(self, master_c):
    """Display IP and port settings UI."""
    self.masterC = master_c
    style = ttk.Style()

    style.configure("Red.TLabel", foreground="red")
    style.configure("Green.TLabel", foreground="green")

    ip_frame = ttk.Frame(master_c)
    frame_width = min(500, self.width - 40)
    ip_frame.place(relx=0.5, rely=0.2, anchor="n", width=frame_width, height=84)

    vip_cmd = (ip_frame.register(lambda p: validate_ip(self, p)), "%P")
    vport_cmd = (ip_frame.register(lambda p: validate_port(self, p)), "%P")

    ip_settings_var = ttk.Entry(
        ip_frame,
        validate="focusout",
        validatecommand=vip_cmd,
    )

    ip_settings_var.delete(0, tk.END)
    ip_settings_var.insert(0, getdata("ip_address"))

    ip_settings_var.configure(font=("Arial", 18))
    ip_settings_var.place(x=5, y=5, width=220, height=40)

    port_settings_var = ttk.Entry(
        ip_frame,
        validate="focusout",
        validatecommand=vport_cmd,
    )

    port_settings_var.delete(0, tk.END)
    port_settings_var.insert(0, getdata("port"))

    port_settings_var.configure(font=("Arial", 18))
    port_settings_var.place(x=230, y=5, width=100, height=40)

    self.connectionStatus = ttk.Label(
        ip_frame,
        text="STATUS",
    )
    self.connectionStatus.configure(font=("Arial", 16))
    self.connectionStatus.place(x=335, y=5, width=100, height=40)

    if test_connection() is not None:
        self.connectionStatus.configure(style="Green.TLabel")
    else:
        self.connectionStatus.configure(style="Red.TLabel")
def handle_reconnection(self):
    """Reconnect to AHM device and update connection status."""
    self.connectionStatus.configure(style="Red.TLabel")
    restart_connection()

    if test_connection() is not None:
        self.connectionStatus.configure(style="Green.TLabel")
    else:
        self.connectionStatus.configure(style="Red.TLabel")



def validate_port(self, port_str, debug=False):
    """Validate port number (0-65535)."""
    try:
        port = int(port_str)
        if 0 <= port <= 65535:
            savedata("port", port)
            if not debug:
                handle_reconnection(self)
            return True
    except ValueError:
        pass
    return False

def validate_ip(self, ip_str, debug=False):
    """Validate IP address (dotted decimal notation)."""
    try:
        parts = ip_str.split(".")
        if len(parts) != 4:
            raise ValueError("IP address must have 4 parts.")
        for part in parts:
            num = int(part)
            if not (0 <= num <= 255):
                raise ValueError("Each part of IP must be between 0 and 255.")
        savedata("ip_address", ip_str)
        if not debug:
            handle_reconnection(self)
        return True
    except ValueError:
        return False



def savedata(label, value):
    """Save configuration value to JSON file."""
    with open("src/cfg.json", "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    data["TCP"][label] = value

    with open("src/cfg.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)      

def getdata(label):
    """Retrieve configuration value from JSON file."""
    with open("src/cfg.json", "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    return data["TCP"][label]

def prompt_password(self, master_c):
    """Display password prompt overlay."""
    self.password_overlay = ttk.Frame(master_c, style="Dark.TFrame")

    self.password_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    dialog_frame = ttk.Frame(
        self.password_overlay, padding=40, bootstyle="secondary"
    )
    dialog_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=min(720, self.width - 40),
        height=min(320, self.height - 40),
    )

    label = ttk.Label(
        dialog_frame, text="Enter Password", font=("Arial", 16)
    )
    label.pack(pady=16)

    self.password_entry = ttk.Entry(
        dialog_frame, show="*", font=("Arial", 14)
    )
    self.password_entry.pack(pady=8)
    self.password_entry.focus_set()

    submit_button = ttk.Button(
        dialog_frame,
        text="Submit",
        width=12,
        bootstyle="primary",
        style="Dialog.TButton",
        command=lambda: check_password(self=self),
    )
    submit_button.pack(side="left", padx=24, pady=16)

    cancel_button = ttk.Button(
        dialog_frame,
        text="Cancel",
        width=12,
        bootstyle="secondary",
        style="Dialog.TButton",
        command=self.password_overlay.destroy,
    )
    cancel_button.pack(side="right", padx=24, pady=16)

def check_password(self):
    """Check password and open settings if correct."""
    password = self.password_entry.get()
    if verify_pass("admin", password):
        print("Password correct")
        self.password_overlay.destroy()
        self.open_settings()
    else:
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(style="Red.TEntry")
