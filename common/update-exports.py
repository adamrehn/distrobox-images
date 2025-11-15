#!/usr/bin/env python3
import os, shutil, subprocess, sys
from pathlib import Path


# Prints and executes a command
def run(command, **kwargs):
	command = list([str(c) for c in command])
	print(command, file=sys.stderr, flush=True)
	return subprocess.run(command, **{'check': True, **kwargs})

# Captures the output of a command
def capture(command, **kwargs):
	try:
		return run(command, **{'capture_output': True, 'encoding': 'utf-8', **kwargs})
	except subprocess.CalledProcessError as err:
		print(f'stdout:\n{ err.stdout }', file=sys.stderr, flush=True)
		print(f'stderr:\n{ err.stderr }', file=sys.stderr, flush=True)
		raise err from None

# Parses an environment variable that represents a list of unique items
def parse_environment_set(key, delim):
	value = os.environ.get(key, '').strip()
	items = value.split(delim) if len(value) > 0 else []
	items = [i.strip() for i in items if len(i) > 0]
	return sorted(set(items))

# Retrieves the list of existing exports for the Distrobox container
def list_exported(export_type, container_id):
	
	# Attempt to query the exports of the specified type
	output = capture(['distrobox-export', f'--list-{ export_type }'])
	
	# Iterate over each line and extract the name of each export
	exports = {}
	lines = output.stdout.splitlines()
	for line in lines:
		components = line.split('|', 1)
		if len(components) == 2:
			
			# Extract the filename of the export
			exported_path = Path(components[1].strip())
			name = exported_path.stem
			
			# Application .desktop files are prefixed with the container ID, so remove it
			if exported_path.suffix == '.desktop':
				name = name.removeprefix(f'{ container_id }-')
			
			# Add the export details to our list
			exports[name] = exported_path
	
	return exports

# Creates an export for the specified application
def export_application(application):
	run(['distrobox-export', '--app', application])

# Creates an export for the specified binary
def export_binary(binary):
	
	# Attempt to resolve the absolute path to the specified binary
	binary_path = shutil.which(binary)
	if binary_path is None:
		raise RuntimeError(f'could not find binary "{ binary }" in the PATH')
	
	# Create the export
	run(['distrobox-export', '--bin', binary_path])


# Verify that we are running inside a Distrobox container
container_id = os.environ.get('CONTAINER_ID')
if container_id is None:
	raise RuntimeError('this script must be run inside a Distrobox container')

# Retrieve the list of applications and binaries we should export
desired_exported_apps = parse_environment_set('CONTAINER_EXPORTED_APPS', ',')
desired_exported_bins = parse_environment_set('CONTAINER_EXPORTED_BINS', ',')

# Remove `~/.local/bin` from the PATH to ensure we can correctly identify the container filesystem location for binaries
local_bin = str(Path('~/.local/bin').expanduser())
path_entries = os.environ.get('PATH').split(':')
path_entries = [e for e in path_entries if e != local_bin]
os.environ['PATH'] = ':'.join(path_entries)

# Print our environment information to assist when debugging
print('', flush=True)
print(Path(__file__).resolve(), flush=True)
print(f'CONTAINER_EXPORTED_APPS: { desired_exported_apps }', flush=True)
print(f'CONTAINER_EXPORTED_BINS: { desired_exported_bins }', flush=True)
print(f'PATH:\n{ path_entries }', flush=True)

# Retrieve the list of applications that are currently exported by the container, and delete any that are not in our list
print('\nRetrieving existing application exports...', flush=True)
existing_exported_apps = list_exported('apps', container_id)
for application, exported_path in existing_exported_apps.items():
	if application not in desired_exported_apps:
		print(f'\nRemoving stale export for application "{ application }": { exported_path }', flush=True)
		exported_path.unlink()

# Retrieve the list of binaries that are currently exported by the container, and delete any that are not in our list
print('\nRetrieving existing binary exports...', flush=True)
existing_exported_bins = list_exported('binaries', container_id)
for binary, exported_path in existing_exported_bins.items():
	if binary not in desired_exported_bins:
		print(f'\nRemoving stale export for binary "{ binary }": { exported_path }', flush=True)
		exported_path.unlink()

# Create or update the exports for each of our exported applications
for application in desired_exported_apps:
	action = 'Updating' if application in existing_exported_apps else 'Creating'
	print(f'\n{ action } export for application "{ application }"...', flush=True)
	export_application(application)

# Create or update the exports for each of our exported binaries
for binary in desired_exported_bins:
	action = 'Updating' if binary in existing_exported_bins else 'Creating'
	print(f'\n{ action } export for binary "{ binary }"...', flush=True)
	export_binary(binary)
