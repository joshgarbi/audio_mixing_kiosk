echo "Launching GUI..."
# 'sg' allows us to run the command with the new group permissions immediately
export WLR_RENDERER=pixman
sg video -c "sg render -c 'cage -- .venv/bin/python3 src/gui.py'"