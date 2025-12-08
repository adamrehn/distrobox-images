FROM adamrehn/distrobox-base-ubuntu:24.04

# Install klogg
ARG KLOGG_DEB_URL="https://github.com/variar/klogg/releases/download/v22.06/klogg-22.06.0.1289-Linux-amd64-jammy.deb"
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	curl -fSL "$KLOGG_DEB_URL" -o /tmp/klogg.deb && \
	apt install -y /tmp/klogg.deb && \
	rm /tmp/klogg.deb

# Configure klogg's .desktop file to ensure the icon will display correctly when exported to the host
# (Note: Distrobox will prefix icon paths with `/run/host` if they're in a standard location, so we symlink the icon elsewhere to avoid this)
RUN ln -s /usr/share/icons/hicolor/scalable/apps/klogg.svg /opt/klogg.svg && \
	sed -i 's|Icon=klogg|Icon=/opt/klogg.svg\nStartupWMClass=klogg|' /usr/share/applications/klogg.desktop

# Configure the container's exports
RUN <<'EOT' bash
	EXPORTS=(
		
		# Export the application shortcut for klogg
		klogg.desktop
		
	)
	
	# Resolve our exports and save the list
	echo "${EXPORTS[@]}" | save-exports.py
	
EOT
