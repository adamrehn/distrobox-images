#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOOLS_DIR="$HOME/.local/bin/distrobox-tools"
SERVICE='distrobox-start-all'
set -ex

# Copy the Python script into place
mkdir -p "$TOOLS_DIR"
cp "$SCRIPT_DIR/start-all.py" "$TOOLS_DIR/start-all.py"

# Create the systemd user unit
cat << "EOF" > "$HOME/.config/systemd/user/$SERVICE.service"
[Unit]
Description=Start all Distrobox containers

[Service]
Type=oneshot
ExecStart=/bin/bash -c "python3 \"$HOME/.local/bin/distrobox-tools/start-all.py\""
RemainAfterExit=yes

[Install]
WantedBy=default.target
EOF

# Enable the service so it runs every time the user logs in
systemctl --user daemon-reload
systemctl --user enable "$SERVICE"
