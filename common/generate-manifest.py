#!/usr/bin/env python3
import argparse, json, os
from pathlib import Path

# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True, help='The name for the Distrobox container')
parser.add_argument('--image', required=True, help='The container image tag')
parser.add_argument('--outfile', required=True, help='The path to the output manifest file')
parser.add_argument('--options', action='append', help='Additional options to include in the manifest')
args = parser.parse_args()

# Retrieve the list of applications and binaries we should export
exports = {}
with open('/container-exports.json', 'r') as infile:
	exports = json.load(infile)

# Verify that our exports are well-formed
if 'applications' not in exports or 'binaries' not in exports or not isinstance(exports['binaries'], dict):
	raise RuntimeError('the container exports JSON file is malformed')

# Generate our manifest
extra_options = [] if args.options is None else args.options
manifest = '\n'.join(
	[
		f'[{ args.name }]',
		f'image="{ args.image }"',
		'replace=true',
		'entry=false',
	] +
	extra_options +
	[f'exported_apps="{ app }"' for app in exports['applications'].values()] +
	[f'exported_bins="{ bin }"' for bin in exports['binaries'].values()] +
	['']
)

# Write the manifest to file
Path(args.outfile).write_text(manifest, 'utf-8')
