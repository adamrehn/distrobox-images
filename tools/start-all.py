#!/usr/bin/env python3
import subprocess


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
		raise RuntimeError('\n'.join([
			f'command { command } failed with exit code { err.returncode } and output:',
			f'stdout: { err.stdout }',
			f'stderr: { err.stderr }'
		])) from None


# Query the list of Distrobox containers, filtering out any malformed entries (see: <https://github.com/89luca89/distrobox/issues/2084>)
lines = capture(['distrobox', 'list', '--no-color']).stdout.splitlines()
parsed = [[field.strip() for field in line.split(' | ')] for line in lines][1:]
containers = [fields[1] for fields in parsed if len(fields) > 2 and not fields[1].startswith(',')]

# Start any containers that aren't already running
for container in containers:
	run(['distrobox', 'enter', container, '--', 'touch', '/dev/null'], check=False)
