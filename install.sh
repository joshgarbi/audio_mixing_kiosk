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

#DEPRECATED
# Define the user and the specific command
# TARGET_USER=$(whoami)
# RULE_FILE="/etc/sudoers.d/netplan-nopasswd"

# echo "Adding passwordless sudo rule for netplan..."

# # Use a heredoc to create the rule file. 
# # We use sudo tee so the script can write to /etc/ even if run without full root initially.
# echo "$TARGET_USER ALL=(ALL) NOPASSWD: /etc/netplan/50-cloud-init.yaml" | sudo tee $RULE_FILE > /dev/null

# # Crucial: sudoers.d files MUST have 0440 permissions or they are ignored for security
# sudo chmod 0440 $RULE_FILE

# echo "Rule created at $RULE_FILE"

sudo chmod 666 /etc/netplan/50-cloud-init.yaml

echo "Setting up autostart with systemd..."

LOCAL_SERVICE_FILE="resources/kiosk.service"
SYSTEM_SERVICE_FILE="/etc/systemd/system/kiosk.service"
# Copy the service file to systemd directory
sudo cp $LOCAL_SERVICE_FILE $SYSTEM_SERVICE_FILE
# set permissions
sudo chmod 644 $SYSTEM_SERVICE_FILE
# Reload systemd to recognize the new service
sudo systemctl daemon-reload
# Enable the service to start on boot
sudo systemctl enable kiosk.service

echo "--- Kiosk Setup Complete ---"

