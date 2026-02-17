# TK Interface and Bootstrap
### [Tkinter](https://docs.python.org/3/library/tkinter.html)
    The tk interface is a light python interface to the Tk GUI toolkit. 

### [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/)
    ttkbootstrap builds upon tkinter with addtional styling, formating, and additional functionality. It makes tkinter feel similar to web development with the comination of constraints and styling. 

## This Project

### [gui.py](../src/gui.py)
    The "main" of this project. Execute this file to run the kiosk with all features. Handles the base canvas and power/settings menue icons internally ip settings popup is handled in the ui helper

### [uihelper.py](../src/uihelper.py)

    Takes some of the work from the main gui file to keep files cleaner and more organized. Manages settings window items and acts as a interface between GUI and the Fader class. It also updates cfg file based on user input for settings.

### [fader.py](../src/fader.py)

    Creates a fader UI object according to listed constraints. Each fader object has a meter and level values associated with it.

### [audiometer.py](../src/audiometer.py)

    Determining the meter colors is a bit complicated. This file handles the color value for the meter based on height from base and changes color. It uses an alpha layer to modulate the meter

### [ahm_control.py](../src/ahm_control.py) 
#### *NEEDS EDIT*

    Currently in development. Will act as the interface between the gui helper and the Allen & Heath AHM TCP API
