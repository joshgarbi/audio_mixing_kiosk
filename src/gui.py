"""Main GUI application for audio mixing kiosk interface."""
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from uihelper import drawfaderbank, ip_settings, preamp_settings, prompt_password
from ahm_control import initialize_connection, close_connection
import sys
import os

## Most code was generated with ChatGPT 5.2 and rewritten to fit needs

class SimpleApp:
    """Main application window for audio mixing kiosk."""

    def __init__(self, width, height, master):
        """Initialize the application with UI components."""
        self.master = master

        self.width = width
        self.height = height

        style = ttk.Style()
        # Configure button styles
        style.configure("danger.TButton", font=("Arial", 24), padding=8)
        style.configure("Dialog.TButton", font=("Arial", 14), padding=8)
        style.configure("secondary.TButton", font=("Arial", 20), padding=8)
        style.configure(
            "tertiary.TButton",
            font=("Arial", 20),
            padding=8,
            background="#0082ec",
            hoverbackground="#007add",
        )
        style.configure("tertiary.TFrame", background="#1e1e1e")
        style.configure(
            "phmpOn.TButton",
            font=("Arial", 14),
            padding=0,
            background="#6A0DAD",
            bordercolor="#6A0DAD"
        )
        style.configure(
            "phmpOff.TButton",
            font=("Arial", 14),
            padding=0,
            background="#363C4D",
            bordercolor="#363C4D"
        )
        style.configure(
            "phmpTest.TButton",
            font=("Arial", 14),
            padding=0,
            background="#FF0077",
            bordercolor="#FF3974"
        )


        drawfaderbank(self, master)

        pil_image = Image.open("resources/power.png")
        pil_image = pil_image.resize((48, 48))
        self.tk_image = ImageTk.PhotoImage(pil_image)

        self.button = ttk.Button(
            master,
            image=self.tk_image,
            bootstyle="danger",
            command=self.quit_app,
        )

        self.button.configure(style="danger.TButton")
        self.button.place(x=12, y=12, width=84, height=84)

        # Settings button in bottom left
        self.settings_button = ttk.Button(
            master,
            text="⚙",
            bootstyle="secondary",
            command=lambda: prompt_password(self, master),
        )
        self.settings_button.configure(style="secondary.TButton")
        self.settings_button.place(
            x=12, y=self.height - 96, width=84, height=84
        )
    def quit_app(self):
        """Show power-off confirmation dialog."""
        # Create the full-screen overlay to block the main UI
        self.exit_overlay = ttk.Frame(self.master, style="Dark.TFrame")
        self.exit_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create the centered dialog
        dialog_frame = ttk.Frame(self.exit_overlay, padding=40, bootstyle="secondary")
        dialog_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=min(680, self.width - 40),
            height=min(340, self.height - 40),
        )

        label = ttk.Label(
            dialog_frame,
            text="Power Off?",
            font=("Arial", 24),
            bootstyle="inverse-secondary",
            foreground="white",
        )
        label.pack(pady=16)

        yes_button = ttk.Button(
            dialog_frame, width=10, text="Shut Down", bootstyle="danger",
            command=lambda: self.shutdown(soft=False)
        )
        yes_button.pack(side="left", padx=20, pady=16)
        no_button = ttk.Button(
            dialog_frame,
            width=12,
            text="Cancel",
            style="tertiary.TButton",
            command=self.exit_overlay.destroy,
        )
        no_button.pack(side="right", padx=20, pady=16)

    def open_settings(self):
        """Open settings panel overlay."""
        self.settings_window = ttk.Frame(self.master, style="Dark.TFrame")
        self.settings_window.place(relx=0, rely=0, relwidth=1, relheight=1)

        label = ttk.Label(
            self.settings_window,
            text="Settings",
            font=("Arial", 24),
            background="#363C4D",
            foreground="white",
        )
        label.pack(pady=20)
        
        self.settings_button = ttk.Button(
            self.settings_window,
            text="Soft Exit",
            bootstyle="tertiary",
            style="Dialog.TButton",
            command=lambda: self.shutdown(soft=True),
        )
        self.settings_button.pack(side="bottom", padx=30, pady=20)
        
        escape_button = ttk.Button(
            self.settings_window,
            width=16,
            text="Close Settings",
            bootstyle="secondary",
            style="Dialog.TButton",
            command=self.settings_window.destroy,
        )
        escape_button.pack(side="bottom", padx=30, pady=16)

        menu_frame = ttk.Frame(self.settings_window)
        menu_frame.pack(pady=10)
        network_button = ttk.Button(
            menu_frame,
            width=16,
            text="Network Settings",
            bootstyle="tertiary",
            style="Dialog.TButton",
            command=lambda: self.show_settings_panel("network"),
        )
        network_button.pack(side="left", padx=10)
        audio_button = ttk.Button(
            menu_frame,
            width=16,
            text="Audio Settings",
            bootstyle="tertiary",
            style="Dialog.TButton",
            command=lambda: self.show_settings_panel("audio"),

        )
        audio_button.pack(side="left", padx=10)
        
        

    def show_settings_panel(self, panel_type):
        """Display the selected settings panel.

        Destroy any previously-created settings panel before showing the new one.
        """
        # destroy previous panels if present
        for attr in ("network_panel", "preamp_panel"):
            if hasattr(self, attr) and getattr(self, attr) is not None:
                try:
                    getattr(self, attr).destroy()
                except AttributeError:
                    pass
                setattr(self, attr, None)

        match panel_type:
            case "network":
                ip_settings(self, self.settings_window)
            case "audio":
                preamp_settings(self, self.settings_window)

    def shutdown(self, soft=False):
        """Close AHM connection and shut down application."""
        if soft:
            close_connection()
            self.master.destroy()
            print("Soft exit - application closed but system remains on.")
            sys.exit(0)
        else:
            close_connection()
            self.master.destroy()
            print("Shutting down system...")
            os.system("sudo shutdown now")
        

if __name__ == "__main__":
    # Kiosk features
    app = ttk.Window(themename="darkly", scaling=1.5)
    MAIN_WIDTH = 800
    MAIN_HEIGHT = 480
    print(f"Screen size: {MAIN_WIDTH}x{MAIN_HEIGHT}")
    initialize_connection()  # Establish AHM connection at startup
    SimpleApp(MAIN_WIDTH, MAIN_HEIGHT, app)
    app.attributes("-fullscreen", True)
    app.resizable(False, False)
    app.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable window closing
    app.mainloop()
