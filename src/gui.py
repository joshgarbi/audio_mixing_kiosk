import tkinter as tk  # Add at top of file
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
from PIL import Image, ImageTk
from audiometer import GradientAudioMeter, change_fader1_value, update_fader1_level
from uihelper import drawfaderbank, ip_settings

## Most code was generated with ChatGPT 5.2 and rewritten to fit needs

class SimpleApp:
    def __init__(self, width, height, master):
        self.master = master
        
        self.width = width     
        self.height = height   
        
        style = ttk.Style()
        # Configure a red (danger) button style with larger font/padding
        style.configure("danger.TButton", font=("Arial", 46), padding=16,)
        style.configure("Dialog.TButton", font=("Arial", 18), padding=12)
        style.configure("secondary.TButton", font=("Arial", 36), padding=12)
        style.configure("tertiary.TFrame", background="#FF00B3")
        
        drawfaderbank(self, master)
        
        pil_image = Image.open("power.png")
        pil_image = pil_image.resize((75, 75))
        self.tk_image = ImageTk.PhotoImage(pil_image)

        self.button = ttk.Button(
            master,
            image=self.tk_image,
            bootstyle="danger",
            command=self.quit_app,  
        )

        self.button.configure(style="danger.TButton")
        self.button.place(x=20, y=20, width=120, height=120)
        
        ## settings button in bottom left to open settings
        self.settings_button = ttk.Button(
            master,
            text="⚙",
            bootstyle="secondary",
            command=self.openSettings,
        )
        self.settings_button.configure(style="secondary.TButton")
        self.settings_button.place(x=20, y=self.height - 140, width=120, height=120)
        
        
    def quit_app(self):
        sure_window = ttk.Toplevel(self.master)
        sure_window.title("Confirm Exit")
        # Frameless dialog
        sure_window.overrideredirect(True)

        dialog_w, dialog_h = 800, 300
        pos_x = max(0, (self.width - dialog_w) // 2)
        pos_y = max(0, (self.height - dialog_h) // 2)
        sure_window.geometry(f"{dialog_w}x{dialog_h}+{pos_x}+{pos_y}")
        sure_window.resizable(False, False)
        sure_window.attributes("-topmost", True)
        
        sure_window.configure(bg="#363C4D")
        sure_window.grab_set()  # Make this window modal
        
        label = ttk.Label(sure_window, text="Power Off?", font=("Arial", 24), background="#363C4D", foreground="white")
        label.pack(pady=20)
        yes_button = ttk.Button(sure_window, width=16, text="Shut Down", bootstyle="danger", style="Dialog.TButton", command=self.master.destroy)
        yes_button.pack(side="left", padx=30, pady=16)
        no_button = ttk.Button(sure_window, width=16, text="Cancel", bootstyle="secondary", style="Dialog.TButton", command=sure_window.destroy)
        no_button.pack(side="right", padx=30, pady=16)
        
    def openSettings(self):
        settings_window = ttk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.overrideredirect(True)  # Frameless dialog
        
        settings_window.geometry(f"{self.width}x{self.height}+0+0")
        settings_window.resizable(False, False)
        settings_window.attributes("-topmost", True)
        
        settings_window.configure(bg="#363C4D")
        settings_window.grab_set()  # Make this window modal
        
        label = ttk.Label(settings_window, text="Settings", font=("Arial", 24), background="#363C4D", foreground="white")
        label.pack(pady=20)
        escape_button = ttk.Button(settings_window, width=16, text="Close Settings", bootstyle="secondary", style="Dialog.TButton", command=settings_window.destroy)
        escape_button.pack(side="bottom", padx=30, pady=16)
        
        # settings_menu()
        
        ip_settings(self, settings_window)


        
if __name__ == "__main__":
    app = ttk.Window(themename="darkly", scaling=1.5) 
    # width = app.winfo_screenwidth()
    # height = app.winfo_screenheight()
    width = 1280
    height = 720
    print(f"Screen size: {width}x{height}")
    SimpleApp(width, height, app)
    app.attributes("-fullscreen", True)
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable window closing
    app.mainloop()