#!/usr/bin/env python3
import subprocess, sys


def run(command, **kwargs):
	command = list([str(c) for c in command])
	return subprocess.run(command, **{'check': True, **kwargs})

def capture(command, **kwargs):
	return run(command, **{'capture_output': True, 'encoding': 'utf-8', **kwargs})


# Wine's default scaling factor is 96 dpi, so we reset it to that if we don't detect a non-default scale factor from the host system
dpi = 96

# Attempt to determine the DPI scale factor used by the host system, and propagate it to Wine
lines = capture(['xrdb', '-query']).stdout.splitlines()
parsed = [[field.strip() for field in line.split(':')] for line in lines]
for fields in parsed:
	if len(fields) > 1 and fields[0] == 'Xft.dpi':
		dpi = int(fields[1])
		break

# Update Wine's scaling factor
run(['wine', 'reg', 'add', 'HKEY_CURRENT_USER\\Control Panel\\Desktop', '/v', 'LogPixels', '/t', 'REG_DWORD', '/d', dpi, '/f'])

# Pass the command-line arguments through to Wine
sys.exit(
	run(['wine'] + sys.argv[1:], check=False).returncode
)
