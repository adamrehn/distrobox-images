#!/usr/bin/env python3
import subprocess, sys


def run(command, **kwargs):
	command = list([str(c) for c in command])
	return subprocess.run(command, **{'check': True, **kwargs})

def capture(command, **kwargs):
	return run(command, **{'capture_output': True, 'encoding': 'utf-8', **kwargs})


# Attempt to determine the DPI scale factor used by the host system, and propagate it to Wine
lines = capture(['xrdb', '-query']).stdout.splitlines()
parsed = [[field.strip() for field in line.split(':')] for line in lines]
for fields in parsed:
	if len(fields) > 1 and fields[0] == 'Xft.dpi':
		run(['wine', 'reg', 'add', 'HKEY_CURRENT_USER\\Control Panel\\Desktop', '/v', 'LogPixels', '/t', 'REG_DWORD', '/d', fields[1], '/f'])
		break

# Pass the command-line arguments through to Wine
sys.exit(
	run(['wine'] + sys.argv[1:], check=False).returncode
)
