#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -ex


# Determine whether we are generating manifests that pull the images from Docker Hub
MANIFEST_OPTIONS=''
if [[ $* == *--live-manifests* ]]; then
	MANIFEST_OPTIONS='--options pull=true'
fi


function generateManifest() {
	local name="$1"
	local image="$2"
	docker run --rm "-v$SCRIPT_DIR:/hostdir" -w /hostdir -u `id -u`:`id -g` "$image" generate-manifest.py \
		--name "$name" \
		--image "$image" \
		--outfile "manifests/$name.ini" \
		$MANIFEST_OPTIONS
}


# Build our base images
docker build --progress=plain -t 'adamrehn/distrobox-base-arch:latest' -f "$SCRIPT_DIR/images/bases/arch/Dockerfile" "$SCRIPT_DIR"
docker build --progress=plain -t 'adamrehn/distrobox-base-ubuntu:24.04' -f "$SCRIPT_DIR/images/bases/ubuntu2404/Dockerfile" "$SCRIPT_DIR"

# Build our Distrobox images
docker build --progress=plain -t 'adamrehn/distrobox-klogg:latest' "$SCRIPT_DIR/images/klogg"
docker build --progress=plain -t 'adamrehn/distrobox-swiss-army-knife:latest' "$SCRIPT_DIR/images/swiss-army-knife"

# Generate the manifests for our Distrobox images
rm -f "$SCRIPT_DIR/manifests/"*.ini
generateManifest 'klogg' 'adamrehn/distrobox-klogg:latest'
generateManifest 'swiss-army-knife' 'adamrehn/distrobox-swiss-army-knife:latest'

# Determine whether we are pushing the images to Docker Hub
if [[ $* == *--push-images* ]]; then
	docker push 'adamrehn/distrobox-base-arch:latest'
	docker push 'adamrehn/distrobox-base-ubuntu:24.04'
	
	docker push 'adamrehn/distrobox-klogg:latest'
	docker push 'adamrehn/distrobox-swiss-army-knife:latest'
fi
