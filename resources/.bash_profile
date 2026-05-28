# If we are on the physical console tty1, launch the Wayland kiosk app
if [[ -z $XDG_RUNTIME_DIR ]]; then
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
fi

if [[ $(tty) == /dev/tty1 ]]; then
    # 1. Inject your custom rendering variable
    export WLR_RENDERER=pixman

    # 2. Run your specific application command execution sequence
    sg video -c "sg render -c 'cage -s -- .venv/bin/python3 src/gui.py'"

    # 3. Clean fallback: If the app closes normally, log out safely
    logout
fi