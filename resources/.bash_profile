# Only trigger the GUI if logging into the main physical monitor console (tty1)
if [[ $(tty) == /dev/tty1 ]]; then
    
    # Define the runtime directory path (1000 is the default primary user ID)
    export XDG_RUNTIME_DIR=/run/user/$(id -u)

    # LOOP: If the directory doesn't exist yet, wait 1 second and check again
    while [ ! -d "$XDG_RUNTIME_DIR" ]; do
        sleep 1
    done
    
    # Inject your specific software rendering pipeline variable
    export WLR_RENDERER=pixman
    
    # Launch Cage with your absolute application paths
    cage -s -- /home/avk/kiosk/audio_mixing_kiosk/.venv/bin/python3 /home/avk/kiosk/audio_mixing_kiosk/src/gui.py
    
    # Developer Exit Protocol
    logout
fi