#!/usr/bin/env python3
import json, os, shutil, sys
from pathlib import Path


# The suffix that we use as a convention to identify exports which represent applications rather than binaries
APPLICATION_SUFFIX = '.desktop'


# Remove `~/.local/bin` from the PATH to ensure we can correctly identify the container filesystem location for binaries
local_bin = str(Path('~/.local/bin').expanduser())
path_entries = os.environ.get('PATH').split(':')
path_entries = [e for e in path_entries if e != local_bin]
os.environ['PATH'] = ':'.join(path_entries)

# Read our list of exports from stdin
exports = sys.stdin.read().split()
processed = {
	'applications': [],
	'binaries': {}
}

# Sort the exports into applications and binaries, and resolve the absolute paths for any binaries
for export in exports:
	if export.endswith(APPLICATION_SUFFIX):
		
		# Strip the suffix, since `distrobox-export` expects either a non-suffixed name or an absolute path
		processed['applications'].append(
			export.removesuffix(APPLICATION_SUFFIX)
		)
		
	else:
		
		# Attempt to resolve the absolute path to the specified binary
		binary = shutil.which(export)
		if binary is None:
			raise RuntimeError(f'could not find binary "{ export }" in the PATH')
		
		# Add the resolved path to our list
		processed['binaries'][export] = binary

# Sort our processed exports and remove any duplicate applications
processed['applications'] = sorted(set(processed['applications']))
processed['binaries'] = dict(sorted(processed['binaries'].items()))

# Write the processed exports to disk for later use by the `apply-exports.py` and `generate-manifest.py` scripts
with open('/container-exports.json', 'w') as outfile:
	json.dump(processed, outfile, indent=True)
