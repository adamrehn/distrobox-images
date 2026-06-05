#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys


def run(command, **kwargs):
	command = list([str(c) for c in command])
	return subprocess.run(command, **{'check': True, **kwargs})


# The USER environment variable isn't set yet when Distrobox init hooks run, so we just infer the username from the home directory
home = Path('~').expanduser()
user = home.name

# Running `host-spawn` won't work as the root user, so we need to do so as the host user
command_exists = lambda binary: run(
	['sudo', '-u', user, 'host-spawn', 'bash', '-c', f'command -v {binary}'], check=False, capture_output=True
).returncode == 0

# Check whether each of the specified commands exists on the host system, and symlink the commands that do exist
for command in sys.argv[1:]:
	if command_exists(command):
		run(['ln', '-s', '/usr/bin/distrobox-host-exec', f'/usr/bin/{command}'])
