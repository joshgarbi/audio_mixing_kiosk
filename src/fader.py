"""Fader widget manager for controlling audio channel levels."""
import json
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, VERTICAL
from audiometer import GradientAudioMeter
from ahm_control import set_ch_level, get_ch_level

with open('src/cfg.json', 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)


class FaderManager:
    """Manager for creating and updating multiple fader widgets."""
    fadersConstrains = data["BANK"]
    master = None

    def __init__(self, master):
        """Initialize FaderManager with master widget."""
        self.master = master
        self.faders = []

    def create_faders(self):
        """Create fader widgets based on configuration."""
        self.master.update_idletasks()
        fader_names = list(self.fadersConstrains.keys())
        fader_count = max(1, len(fader_names))

        bank_width = max(300, self.master.winfo_width())
        bank_height = max(320, self.master.winfo_height())

        side_padding = 8
        gap = 8
        usable_width = bank_width - (side_padding * 2) - (gap * (fader_count - 1))
        fader_width = max(96, usable_width // fader_count)
        fader_height = max(300, bank_height - 20)

        for index, fader_name in enumerate(fader_names):
            x_pos = side_padding + index * (fader_width + gap)
            self.fader = Fader(
                self.master, x_pos, 10, fader_name, fader_width, fader_height
            )
            self.faders.append(self.fader)

    def update_all(self):
        """Update all fader level displays."""
        for self.fader in self.faders:
            self.fader.update_fader_level()


class Fader:
    """Individual fader widget with slider, meter, and level control."""
    fader_level = 0
    update_interval = 100  # milliseconds
    master = None
    api_thread = None

    def __init__(self, master, x, y, label, fader_width, fader_height):
        """Initialize fader widget at specified position."""
        self.master = master
        self.channel = int(label[-1]) - 1

        slider_length = max(180, fader_height - 100)
        slider_width = max(24, min(46, fader_width // 3))
        slider_handle = max(35, min(70, slider_length // 4))
        meter_width = max(12, min(24, fader_width // 5))
        label_size = max(12, min(18, fader_width // 6))

        self.fader1group = ttk.Frame(master, style="tertiary.TFrame")
        self.fader1group.place(x=x, y=y, width=fader_width, height=fader_height)

        self.fader1_container = ttk.Frame(
            self.fader1group, style="TFrame", borderwidth=0
        )
        self.fader1_container.pack(side=LEFT, padx=6)
        self.fader1_label = ttk.Label(
            self.fader1_container,
            text=label,
            font=("Helvetica", label_size),
            background="",
            borderwidth=0,
        )
        self.fader1_label.pack()

        self.fader1slider = tk.Scale(
            self.fader1_container,
            from_=100,
            to=0,
            orient=VERTICAL,
            length=slider_length,
            command=self.change_fader_value,
            bg="#2d7dd2",
            activebackground="#4a9eff",
            troughcolor="#1e1e1e",
            highlightthickness=0,
            sliderlength=slider_handle,
            sliderrelief="solid",
            width=slider_width,
            bd=0,
        )

        self.fader1slider.set(get_ch_level(self.channel))
        self.fader1slider.pack(pady=4)

        self.level1 = GradientAudioMeter(
            self.fader1group, width=meter_width, height=slider_length
        )
        self.level1.pack(side="right", padx=4, pady=24)

    def change_fader_value(self, value):
        """Handle fader value change event."""
        value = int(value)
        set_ch_level(value, self.channel)
        self.fader_level = value

    def update_fader_level(self):
        """Update meter display with current level."""
        level = self.fader1slider.get()
        noise = random.randint(-5, 5)
        level += noise
        self.level1.set_level(level)
        self.master.after(self.update_interval, self.update_fader_level)
    
