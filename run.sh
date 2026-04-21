echo "Launching GUI..."
# 'sg' allows us to run the command with the new group permissions immediately
export WLR_RENDERER=pixman

# Hide the cursor at OS level while the kiosk is running.
UNCLUTTER_PID=""
if command -v unclutter >/dev/null 2>&1; then
	unclutter -idle 0 -root >/dev/null 2>&1 &
	UNCLUTTER_PID=$!
fi

cleanup() {
	if [ -n "$UNCLUTTER_PID" ] && kill -0 "$UNCLUTTER_PID" >/dev/null 2>&1; then
		kill "$UNCLUTTER_PID" >/dev/null 2>&1 || true
	fi
}

trap cleanup EXIT INT TERM

sg video -c "sg render -c 'cage -- .venv/bin/python3 src/gui.py'"