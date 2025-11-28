FROM adamrehn/distrobox-base-ubuntu:24.04

# Install klogg
ARG KLOGG_DEB_URL="https://github.com/variar/klogg/releases/download/v22.06/klogg-22.06.0.1289-Linux-amd64-jammy.deb"
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	curl -fSL "$KLOGG_DEB_URL" -o /tmp/klogg.deb && \
	apt install -y /tmp/klogg.deb && \
	rm /tmp/klogg.deb

# Configure the container's exports
RUN <<'EOT' bash
	EXPORTS=(
		
		# Export the application shortcut for klogg
		klogg.desktop
		
	)
	
	# Resolve our exports and save the list
	echo "${EXPORTS[@]}" | save-exports.py
	
EOT
