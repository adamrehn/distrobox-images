FROM adamrehn/distrobox-base-ubuntu:26.04

# Add the Wine package repository
RUN mkdir -pm755 /etc/apt/keyrings
RUN wget -O - 'https://dl.winehq.org/wine-builds/winehq.key' | gpg --dearmor -o /etc/apt/keyrings/winehq-archive.key -
RUN wget -NP /etc/apt/sources.list.d/ 'https://dl.winehq.org/wine-builds/ubuntu/dists/resolute/winehq-resolute.sources'

# Install the latest stable version of Wine (currently 11.0), along with `x11-xserver-utils` (for xrdb) and Xvfb
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
	apt-get update && apt-get install -y --install-recommends \
		winehq-stable \
		x11-xserver-utils \
		xvfb

# Create a Wine prefix and perform first-run setup
# (Note that the prefix is owned by root during the build process, but our init hook will `chown` it at container startup with the host user's UID and GID)
ENV WINEARCH=wow64
ENV WINEPREFIX=/opt/wineprefixes/prefix
RUN mkdir -p "$WINEPREFIX"
RUN wineboot && wineserver --wait

# Preinstall the appropriate version of Wine Mono (as listed here: <https://gitlab.winehq.org/wine/wine/-/wikis/Wine-Mono#versions>)
ENV MONO_VERSION='10.4.1'
RUN curl -fSL "https://dl.winehq.org/wine/wine-mono/$MONO_VERSION/wine-mono-$MONO_VERSION-x86.msi" -o /tmp/wine-mono-x86.msi && \
	xvfb-run -a wine msiexec /i /tmp/wine-mono-x86.msi && \
	wineserver --wait && \
	rm /tmp/wine-mono-x86.msi

# Copy our Python scripts into the image
COPY images/bases/ubuntu2604-wine/*.py /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py

# Configure an init hook for all containers derived from this base image, which runs `chown` on the Wine prefix
# (Note that the non-escaped `id -u` and `id -g` will be evaluated by the host shell, whereas $WINEPREFIX will be evaluated inside the container)
RUN echo 'chown -R `id -u`:`id -g` \$WINEPREFIX' >> /container-init-hooks.txt
