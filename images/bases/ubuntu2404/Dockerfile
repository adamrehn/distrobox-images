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

# Install Python so we can use it to run our export management scripts
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		python3

# Copy our export management Python scripts into the image
COPY common/*.py /usr/local/bin/
RUN chmod +x /usr/local/bin/*.py
