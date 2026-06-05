#!/usr/bin/env python3
import argparse, json, shutil, subprocess, urllib.request
from pathlib import Path


# Exception type for reporting malformed JSON manifest data
class MalformedManifestError(Exception):
	def __init__(self, path_or_url, reason):
		super().__init__(f'JSON manifest "{ path_or_url }" is malformed: { reason }')


# Prints a log message to stdout and flushes the output
def log(message):
	print(message, flush=True)

# Prints and executes a command
def run(command, dry_run=False, **kwargs):
	command = list([str(c) for c in command])
	log(command)
	if dry_run:
		return None
	else:
		return subprocess.run(command, **{'check': True, **kwargs})

# Captures the output of a command
def capture(command, dry_run=False, **kwargs):
	try:
		return run(command, dry_run=dry_run, **{'capture_output': True, 'encoding': 'utf-8', **kwargs})
	except subprocess.CalledProcessError as err:
		raise RuntimeError('\n'.join([
			f'command { command } failed with exit code { err.returncode } and output:',
			f'stdout: { err.stdout }',
			f'stderr: { err.stderr }'
		])) from None

# Determines if the specified path is a URI
def is_uri(path):
	return '://' in path

# Reads the contents of a local file or a remote URL
def read_input(path_or_url):
	if is_uri(path_or_url):
		with urllib.request.urlopen(path_or_url) as f:
			return f.read().decode('utf-8')
	else:
		return Path(path_or_url).read_text('utf-8')

# Parses the contents of the specified JSON manifest file, recursively resolving any includes
def parse_manifest(path_or_url):
	
	# Parse the JSON data and verify that it is well-formed
	parsed = json.loads(read_input(path_or_url))
	if not isinstance(parsed, dict):
		raise MalformedManifestError(path_or_url, 'root element is not an object')
	for key, value in parsed.items():
		if not isinstance(value, list):
			raise MalformedManifestError(path_or_url, f'field "{ key }" is not an array')
	
	# Recursively resolve any includes and merge their contents into the parsed data
	if 'include' in parsed:
		for include in parsed.get('include', []):
			nested = parse_manifest(include)
			for key, value in nested.items():
				if key in parsed:
					parsed[key] = parsed[key] + value
				else:
					parsed[key] = value
		
		del parsed['include']
	
	return parsed


# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('manifest', help='File path or URL of the JSON manifest file to apply')
parser.add_argument('--dry-run', action='store_true', help='Print commands but do not run them')
args = parser.parse_args()

# Print the specified options
log(f'Manifest:  { args.manifest }')
log(f'Dry Run:   { args.dry_run }')

# Parse the specified manifest file
manifest = parse_manifest(args.manifest)

# Verify that we have the required tools for each list of items that we are installing
if 'distrobox' in manifest and shutil.which('distrobox') is None:
	raise RuntimeError('JSON manifest includes Distrobox manifests to assemble, but Distrobox is not installed')
if 'flatpak' in manifest and shutil.which('flatpak') is None:
	raise RuntimeError('JSON manifest includes Flatpak packages to install, but Flatpak is not installed')

# If any Distrobox manifests were specified then verify that the user has the privileges to interact with the container manager
# (e.g. the `distrobox ls` command will fail if a user doesn't have permission to run Docker commands)
if 'distrobox' in manifest:
	log('\nVerifying that the current user has the required privileges to run Distrobox...')
	capture(['distrobox', 'ls'], dry_run=args.dry_run)

# If any Flatpak packages were specified then ensure Flathub is configured as a remote for the current user
if 'flatpak' in manifest:
	log('\nEnsuring Flathub is configured as a Flatpak remote for the current user...')
	run(['flatpak', 'remote-add', '--user', '--if-not-exists', 'flathub', 'https://dl.flathub.org/repo/flathub.flatpakrepo'], dry_run=args.dry_run)

# Process any Distrobox manifests
if 'distrobox' in manifest:
	items = manifest['distrobox']
	log(f'\nAssembling { len(items) } Distrobox manifest(s)...')
	for item in items:
		run(['distrobox', 'assemble', 'create', '--file', item], dry_run=args.dry_run)

# Process any Flatpak packages
if 'flatpak' in manifest:
	items = manifest['flatpak']
	log(f'\nInstalling { len(items) } Flatpak package(s)...')
	for item in items:
		run(['flatpak', 'install','--user', '-y', 'flathub', item], dry_run=args.dry_run)
