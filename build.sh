#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -ex


function generateManifest() {
	local name="$1"
	local image="$2"
	docker run --rm "-v$SCRIPT_DIR:/hostdir" -w /hostdir -u `id -u`:`id -g` "$image" generate-manifest.py \
		--name "$name" \
		--image "$image" \
		--outfile "manifests/$name.ini"
}


# Build our base images
docker build --progress=plain -t 'adamrehn/distrobox-base-arch:latest' -f "$SCRIPT_DIR/images/bases/arch/Dockerfile" "$SCRIPT_DIR"

# Build our Distrobox images
docker build --progress=plain -t 'adamrehn/distrobox-swiss-army-knife:latest' "$SCRIPT_DIR/images/swiss-army-knife"

# Generate the manifests for our Distrobox images
rm -f "$SCRIPT_DIR/manifests/"*.ini
generateManifest 'swiss-army-knife' 'adamrehn/distrobox-swiss-army-knife:latest'
