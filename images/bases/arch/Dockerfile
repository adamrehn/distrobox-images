FROM quay.io/toolbx/arch-toolbox:latest

# Preinstall the base packages needed by Distrobox, to save time when running `distrobox-init`:
# <https://github.com/89luca89/distrobox/blob/1.8.2.1/distrobox-init#L1333-L1392>
RUN --mount=type=cache,target=/var/cache/pacman,sharing=locked \
	pacman -Syu --needed --noconfirm \
		bash \
		bash-completion \
		bc \
		curl \
		diffutils \
		findutils \
		glibc \
		glibc-locales \
		gnupg \
		iputils \
		inetutils \
		keyutils \
		less \
		lsof \
		man-db \
		man-pages \
		mlocate \
		mtr \
		ncurses \
		nss-mdns \
		openssh \
		pigz \
		pinentry \
		procps-ng \
		rsync \
		shadow \
		sudo \
		tcpdump \
		time \
		traceroute \
		tree \
		tzdata \
		unzip \
		util-linux \
		util-linux-libs \
		vte-common \
		wget \
		words \
		xorg-xauth \
		zip \
		mesa \
		vulkan-intel \
		vulkan-radeon

# Install Python so we can use it to run our export management scripts
RUN --mount=type=cache,target=/var/cache/pacman,sharing=locked \
	pacman -Syu --needed --noconfirm \
		python

# Copy our export management Python scripts into the image
COPY common/*.py /usr/local/bin/
RUN chmod +x /usr/local/bin/apply-exports.py
RUN chmod +x /usr/local/bin/save-exports.py
