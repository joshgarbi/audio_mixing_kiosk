import tkinter as tk  # Add at top of file
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
# from bak.test import GradientAudioMeter
from audiometer import GradientAudioMeter
from ahm_control import setlevel

class FaderManager:
    fadersConstrains = {
        "fader1": [20, 20],
        # "fader2": [220, 20],
        # "fader3": [420, 20],
        # "fader4": [620, 20],
        # "fader5": [820, 20]
    }
    faders = []
    master = None

    def __init__(self, master):
        self.master = master
    
    def createFaders(self):
        for faderName, faderPosition in self.fadersConstrains.items():
            self.fader = Fader(self.master, faderPosition[0], faderPosition[1], faderName)
            self.faders.append(self.fader)
            
    def updateAll(self):
        for self.fader in self.faders:
            self.fader.updateFaderLevel()


class Fader:
    fader_level = 0
    update_interval = 100  # milliseconds
    master = None
    api_thread = None
    def __init__(self, master, x, y, label):
        self.master = master

        self.fader1group = ttk.Frame(master, style="tertiary.TFrame")
        self.fader1group.place(x=x, y=y, width=175, height=675)
    
        self.fader1_container = ttk.Frame(self.fader1group, style="TFrame", borderwidth=0)
        self.fader1_container.pack(side=LEFT, padx=10)
        self.fader1_label = ttk.Label(self.fader1_container, text=label, font=("Helvetica", 24), background="", borderwidth=0)    
        self.fader1_label.pack()
        
        self.fader1slider = tk.Scale(self.fader1_container, from_=100, to=0, orient=VERTICAL, length=800, 
            command=self.changeFaderValue,
            bg='#2d7dd2', activebackground='#4a9eff',
            troughcolor='#1e1e1e', highlightthickness=0,
            sliderlength=160, sliderrelief='solid', width=75, bd=0)
        
        
        self.fader1slider.set(0)
        self.fader1slider.pack(pady=5)
        
        self.level1 = GradientAudioMeter(self.fader1group, width=50, height=800)
        self.level1.pack(side="right", pady=15)

    def changeFaderValue(self, value):
        value = int(value)
        setlevel(value)
        self.fader_level = value

    def updateFaderLevel(self):
        level = self.fader1slider.get()
        noise = random.randint(-5,5)
        level += noise
        self.level1.set_level(level)
        self.master.after(self.update_interval, self.updateFaderLevel)
    
