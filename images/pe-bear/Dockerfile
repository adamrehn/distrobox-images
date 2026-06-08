FROM adamrehn/distrobox-base-ubuntu:26.04

# Install PE-Bear's Qt dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	apt-get update && apt-get install -y --no-install-recommends \
		libqt6gui6 \
		libqt6widgets6

# Install PE-Bear
ARG PEBEAR_TARBALL_URL="https://github.com/hasherezade/pe-bear/releases/download/v0.7.2/PE-bear_0.7.2_qt6.4.2_x64_linux.tar.xz"
RUN curl -fSL "$PEBEAR_TARBALL_URL" -o /tmp/pebear.tar.xz && \
	mkdir /tmp/extracted && \
	tar --directory=/tmp/extracted --strip-components=1 -xf /tmp/pebear.tar.xz && \
	cd /tmp/extracted && \
	./install.sh && \
	rm -rf /tmp/extracted && \
	rm /tmp/pebear.tar.xz

# Configure PE-Bear's .desktop file to ensure the icon will display correctly when exported to the host
# (Note: Distrobox won't copy the icon to the host filesystem if it's in the default location, so we symlink the icon elsewhere to avoid this)
RUN ln -s /usr/local/share/pixmaps/net.hasherezade.pe-bear.png /opt/net.hasherezade.pe-bear.png && \
	sed -i 's|Icon=net.hasherezade.pe-bear|Icon=/opt/net.hasherezade.pe-bear.png\nStartupWMClass=PE-bear|' /usr/local/share/applications/net.hasherezade.pe-bear.desktop

# Configure the container's exports
RUN <<'EOT' bash
	EXPORTS=(
		
		# Export the application shortcut for PE-Bear
		net.hasherezade.pe-bear.desktop
		
	)
	
	# Resolve our exports and save the list
	echo "${EXPORTS[@]}" | save-exports.py
	
EOT
