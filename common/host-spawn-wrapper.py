#!/usr/bin/env python3
import os, subprocess, sys


# Runs the real version of `host-spawn` with the specified arguments
def run_host_spawn(args):
	result = subprocess.run(['/opt/real-host-spawn/host-spawn'] + args)
	sys.exit(result.returncode)


# If a version or help flag was specified (or no arguments at all) then don't modify the arguments
if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', '--version']:
	run_host_spawn(sys.argv[1:])


# Retrieve the list of environment variables that should be propagated to the host process
env_vars = os.environ.get('HOST_EXEC_PROPAGATED_ENV_VARS', '')
env_vars = f'TERM,{env_vars}' if len(env_vars) > 0 else 'TERM'

# Inject a command-line flag to propagate the environment variables
args = ['--env', env_vars] + sys.argv[1:]
run_host_spawn(args)
