if [[ $(tty) == /dev/tty1 ]]; then
    
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
    while [ ! -d "$XDG_RUNTIME_DIR" ]; do
        sleep 0.5
    done
    
    # 1. MOVE INTO YOUR PROJECT DIRECTORY FIRST
    # This aligns Python's relative path lookups with your files
    cd /home/avk/kiosk/audio_mixing_kiosk
    
    # 2. Set up your rendering flags
    export WLR_RENDERER=pixman
    export WLR_BACKENDS=drm,libinput
    export XDG_SEAT=seat0
    
    # 3. Launch Cage using paths relative to this directory
    # Notice we can use local paths now because 'cd' placed us in the right folder
    exec cage -s -- .venv/bin/python3 src/gui.py
fi