set -e

echo "--- Starting Kiosk Setup ---"

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

# 5. Remove cursor icon if exists
echo "Removing cursor icon..."
# Backup the original cursor just in case
sudo mv /usr/share/icons/Adwaita/cursors/left_ptr /usr/share/icons/Adwaita/cursors/left_ptr.bak

# Create a symlink to a non-existent or empty file
sudo ln -s /dev/null /usr/share/icons/Adwaita/cursors/left_ptr