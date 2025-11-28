#!/usr/bin/env python3
import json, os, subprocess
from pathlib import Path


# Prints a log message to stdout and flushes the output
def log(message):
	print(message, flush=True)

# Prints and executes a command
def run(command, **kwargs):
	command = list([str(c) for c in command])
	log(command)
	return subprocess.run(command, **{'check': True, **kwargs})

# Captures the output of a command
def capture(command, **kwargs):
	try:
		return run(command, **{'capture_output': True, 'encoding': 'utf-8', **kwargs})
	except subprocess.CalledProcessError as err:
		log(f'stdout:\n{ err.stdout }')
		log(f'stderr:\n{ err.stderr }')
		raise err from None

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
			name = exported_path.name
			
			# Application .desktop files are prefixed with the container ID, so remove it
			if exported_path.suffix == '.desktop':
				name = name.removeprefix(f'{ container_id }-')
			
			# Add the export details to our list
			exports[name] = exported_path
	
	return exports


# Verify that we are running inside a Distrobox container
container_id = os.environ.get('CONTAINER_ID')
if container_id is None:
	raise RuntimeError('this script must be run inside a Distrobox container')

# Retrieve the list of applications and binaries we should export
exports = {}
with open('/container-exports.json', 'r') as infile:
	exports = json.load(infile)

# Verify that our exports are well-formed
if 'applications' not in exports or 'binaries' not in exports or not isinstance(exports['binaries'], dict):
	raise RuntimeError('the container exports JSON file is malformed')

# Retrieve the list of applications that are currently exported by the container, and delete any that are not in our list
log('\nRetrieving existing application exports...')
existing_apps = list_exported('apps', container_id)
for application, exported_path in existing_apps.items():
	if application not in exports['applications']:
		log(f'\nRemoving stale export for application "{ application }": { exported_path }')
		exported_path.unlink()

# Retrieve the list of binaries that are currently exported by the container, and delete any that are not in our list
log('\nRetrieving existing binary exports...')
existing_bins = list_exported('binaries', container_id)
for binary, exported_path in existing_bins.items():
	if binary not in exports['binaries'].keys():
		log(f'\nRemoving stale export for binary "{ binary }": { exported_path }')
		exported_path.unlink()

# Create or update the exports for each of our exported applications
for name, application in exports['applications'].items():
	action = 'Updating' if name in existing_apps else 'Creating'
	log(f'\n{ action } export for application "{ name }"...')
	run(['distrobox-export', '--app', application])

# Create or update the exports for each of our exported binaries
for name, binary in exports['binaries'].items():
	action = 'Updating' if name in existing_bins else 'Creating'
	log(f'\n{ action } export for binary "{ name }"...')
	run(['distrobox-export', '--bin', binary])
