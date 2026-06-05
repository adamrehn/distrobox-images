#!/usr/bin/env python3
import argparse, os, subprocess
from pathlib import Path


def run(command, **kwargs):
	command = list([str(c) for c in command])
	return subprocess.run(command, **{'check': True, **kwargs})


# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('host_subpath', help="Target subpath under the host user's home directory")
parser.add_argument('wine_subpath', help="Symlink subpath in the Wine prefix, under C:/Users/<USER>")
args = parser.parse_args()

# Retrieve the path to the Wine prefix and the user's home directory
prefix = Path(os.environ['WINEPREFIX'])
home = Path('~').expanduser()

# The USER environment variable isn't set yet when Distrobox init hooks run, so we just infer the username from the home directory
user = home.name

# When we create directories and symlinks, we do so as the user to ensure they own the created files
run_as_user = lambda command: run(['sudo', '-u', user] + command)

# Resolve the full paths for the Wine path and the host path
wine_path = prefix / 'drive_c' / 'users' / user / args.wine_subpath
host_path = home / args.host_subpath

# If the subpath under the user's home directory doesn't exist then create it
if not host_path.exists():
	run_as_user(['mkdir', '-p', host_path])

# If the Wine path already exists then remove it, taking care to remove just the symlink itself if it's already in place
if wine_path.is_symlink():
	run(['rm', wine_path])
else:
	run(['rm', '-rf', wine_path])

# Symlink the Wine path to the host path, ensuring any parent directories in the Wine path exist
run_as_user(['mkdir', '-p', wine_path.parent])
run_as_user(['ln', '-s', host_path, wine_path])
