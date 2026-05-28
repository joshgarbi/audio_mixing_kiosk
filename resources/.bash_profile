# Only trigger the GUI if logging into the main physical monitor console (tty1)
if [[ $(tty) == /dev/tty1 ]]; then

    # 1. Set up the local runtime environment directory
    export XDG_RUNTIME_DIR=/run/user/$(id -u)

    # 2. Inject your specific software rendering pipeline variable
    export WLR_RENDERER=pixman

    # 3. Launch Cage with your absolute application paths
    cage -s -- /home/avk/kiosk/audio_mixing_kiosk/.venv/bin/python3 /home/avk/kiosk/audio_mixing_kiosk/src/gui.py

    # 4. Developer Exit Protocol
    # If the Python app closes cleanly via an admin exit, log out back to the terminal.
    # If it closes via a system shutdown command, the OS will turn off before hitting this.
    logout
fi