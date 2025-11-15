#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -ex

# Build our base images
docker build --progress=plain -t 'adamrehn/distrobox-base-arch:latest' -f "$SCRIPT_DIR/images/bases/arch/Dockerfile" "$SCRIPT_DIR"

# Build our Distrobox images
docker build --progress=plain -t 'adamrehn/distrobox-swiss-army-knife:latest' "$SCRIPT_DIR/images/swiss-army-knife"
