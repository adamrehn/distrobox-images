FROM quay.io/toolbx/ubuntu-toolbox:24.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Preinstall the base packages needed by Distrobox, to save time when running `distrobox-init`:
# <https://github.com/89luca89/distrobox/blob/1.8.2.1/distrobox-init#L786-L867>
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		apt-utils \
		bash \
		bash-completion \
		bc \
		bzip2 \
		curl \
		dialog \
		diffutils \
		findutils \
		gnupg \
		gnupg2 \
		gpgsm \
		hostname \
		iproute2 \
		iputils-ping \
		keyutils \
		language-pack-en \
		less \
		libcap2-bin \
		libegl1 \
		libegl-mesa0 \
		libgl1 \
		libglx-mesa0 \
		libkrb5-3 \
		libnss-mdns \
		libnss-myhostname \
		libvte-2.9*-common \
		libvte-common \
		libvulkan1 \
		locales \
		lsof \
		man-db \
		manpages \
		mesa-vulkan-drivers \
		mtr \
		ncurses-base \
		openssh-client \
		passwd \
		pigz \
		pinentry-curses \
		procps \
		rsync \
		sudo \
		tcpdump \
		time \
		traceroute \
		tree \
		tzdata \
		unzip \
		util-linux \
		wget \
		xauth \
		xz-utils \
		zip

# Install Python so we can use it to run our export management scripts and `host-spawn` wrapper script
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		python3

# Preinstall the `host-spawn` tool used by `distrobox-host-exec`
ARG HOST_SPAWN_VERSION="v1.6.2"
RUN mkdir -p /opt/real-host-spawn && \
	curl -fSL "https://github.com/1player/host-spawn/releases/download/$HOST_SPAWN_VERSION/host-spawn-x86_64" -o /opt/real-host-spawn/host-spawn && \
	chmod +x /opt/real-host-spawn/host-spawn

# Copy our Python scripts into the image
COPY common/*.py /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py

# Name our `host-spawn` wrapper script so it will be used automatically by `distrobox-host-exec`
RUN ln -s /usr/local/bin/host-spawn-wrapper.py /usr/local/bin/host-spawn
