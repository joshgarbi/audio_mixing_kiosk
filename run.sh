echo "Launching GUI..."
# 'sg' allows us to run the command with the new group permissions immediately
export WLR_RENDERER=pixman
export XCURSOR_SIZE=0
sg video -c "sg render -c 'cage -s -- .venv/bin/python3 src/gui.py'"