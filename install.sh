set -e

echo "--- Starting Kiosk Setup v1.0 ---"

echo "Installing system packages..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-tk cage xwayland libgl1-mesa-dri

# 2. Setup Python Virtual Environment
echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python Requirements
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping pip install."
fi

# 4. Permissions
echo "Setting hardware permissions..."
sudo usermod -aG video,render $USER

# 5. Launch
echo "Launching GUI..."
# 'sg' allows us to run the command with the new group permissions immediately
export WLR_RENDERER=pixman
sg video -c "sg render -c 'cage -- .venv/bin/python3 src/gui.py'"