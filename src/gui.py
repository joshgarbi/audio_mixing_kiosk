import tkinter as tk  # Add at top of file
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from uihelper import drawfaderbank, ip_settings, prompt_password
from ahm_control import initialize_connection, close_connection, restart_connection

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
        style.configure("tertiary.TButton", font=("Arial", 46), padding=16, background="#0082ec", hoverbackground="#007add")
        style.configure("tertiary.TFrame", background="#1e1e1e")
        
        drawfaderbank(self, master)
        
        pil_image = Image.open("resources/power.png")
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
            command=lambda: prompt_password(self, master),
        )
        self.settings_button.configure(style="secondary.TButton")
        self.settings_button.place(x=20, y=self.height - 140, width=120, height=120)
        
        
    def quit_app(self):
        # Create the full-screen overlay to block the main UI
        self.exit_overlay = ttk.Frame(self.master, style="Dark.TFrame")
        self.exit_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    
        # Create the centered "dialog" box inside the overlay
        dialog_frame = ttk.Frame(self.exit_overlay, padding=40, bootstyle="secondary")
        dialog_frame.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=500)
        
        label = ttk.Label(dialog_frame, text="Power Off?", font=("Arial", 32), bootstyle="inverse-secondary", foreground="white")
        label.pack(pady=20)
        
        yes_button = ttk.Button(dialog_frame, width=10, text="Shut Down", bootstyle="danger", command=self.shutdown)
        yes_button.pack(side="left", padx=30, pady=16)
        no_button = ttk.Button(dialog_frame, width=24, text="Cancel", style="tertiary.TButton", command=self.exit_overlay.destroy)
        no_button.pack(side="right", padx=30, pady=16)
        
    def openSettings(self):
        self.settings_window = ttk.Frame(self.master, style="Dark.TFrame")
        self.settings_window.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        
        
        label = ttk.Label(self.settings_window, text="Settings", font=("Arial", 24), background="#363C4D", foreground="white")
        label.pack(pady=20)
        escape_button = ttk.Button(self.settings_window, width=16, text="Close Settings", bootstyle="secondary", style="Dialog.TButton", command=self.settings_window.destroy)
        escape_button.pack(side="bottom", padx=30, pady=16)
        
        # settings_menu()
        
        ip_settings(self, self.settings_window)

    def shutdown(self):
        close_connection()
        self.master.destroy()

    print()
        
if __name__ == "__main__":
    # kiosk features:
    app = ttk.Window(themename="darkly", scaling=1.5) 
    # width = app.winfo_screenwidth()
    # height = app.winfo_screenheight()
    width = 1280
    height = 720
    print(f"Screen size: {width}x{height}")
    initialize_connection()  # Establish AHM connection at startup
    SimpleApp(width, height, app)
    app.attributes("-fullscreen", True)
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable window closing
    app.mainloop()