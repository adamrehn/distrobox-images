FROM adamrehn/distrobox-base-wine:ubuntu26.04

# Install foobar2000
# (Note that we install the 32-bit version, since most of the components we install don't have 64-bit builds)
ENV FOOBAR_VERSION='v2.25.9'
RUN curl -fSL "https://www.foobar2000.org/downloads/foobar2000_$FOOBAR_VERSION.exe" -o /tmp/foobar2000.exe && \
	xvfb-run -a wine /tmp/foobar2000.exe /S && \
	wineserver --wait

# Install the VIOGSF component
RUN curl -fSL 'http://vgmpf.com/Wiki/images/6/6a/VIOGSF_v0.08.16.zip' -o /tmp/VIOGSF.zip && \
	unzip /tmp/VIOGSF.zip -d /tmp/VIOGSF && \
	cp /tmp/VIOGSF/foo_input_viogsf.dll "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	cp /tmp/VIOGSF/viogsf.bin "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	rm -rf /tmp/VIOGSF && \
	rm /tmp/VIOGSF.zip

# Install the VIO2SF component
RUN curl -fSL 'https://www.foobar2000.org/getcomponent/f1ec0447dbace81269f75452f6febd3a/foo_input_vio2sf.fb2k-component' -o /tmp/foo_input_vio2sf.fb2k-component && \
	unzip /tmp/foo_input_vio2sf.fb2k-component -d "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	rm /tmp/foo_input_vio2sf.fb2k-component

# Install the PSF Decoder component
# (Note that we use a slightly older version here, since the latest release refuses to play certain input files)
RUN curl -fSL 'http://vgmpf.com/Wiki/images/a/ae/PSF_Decoder_v2.0.38.zip' -o /tmp/PSF_Decoder.zip && \
	unzip /tmp/PSF_Decoder.zip -d /tmp && \
	unzip '/tmp/PSF Decoder v2.0.38.fb2k-component' -d "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	rm '/tmp/PSF Decoder v2.0.38.fb2k-component' && \
	rm /tmp/PSF_Decoder.zip

# Install the USF Decoder component
RUN curl -fSL 'https://www.foobar2000.org/getcomponent/18d5e030441f3fef68ffee70fa913122/foo_input_usf.fb2k-component' -o /tmp/foo_input_usf.fb2k-component && \
	unzip /tmp/foo_input_usf.fb2k-component -d "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	rm /tmp/foo_input_usf.fb2k-component

# Install the Game Emu Player component
RUN curl -fSL 'https://www.foobar2000.org/getcomponent/4099469cbbef547344347c4409600d44/foo_gep.fb2k-component' -o /tmp/foo_gep.fb2k-component && \
	unzip /tmp/foo_gep.fb2k-component -d "$WINEPREFIX/drive_c/Program Files (x86)/foobar2000/components/" && \
	rm /tmp/foo_gep.fb2k-component

# Copy the foobar2000 .desktop file and accompanying icons to paths where Distrobox will search for them when exporting to the host system
RUN cp /root/.local/share/applications/wine/Programs/foobar2000.desktop /usr/share/applications/foobar2000.desktop
RUN cp -R /root/.local/share/icons/* /usr/share/icons/

# Rewrite the .desktop file so it points directly to the foobar2000 executable rather than its shortcut file
RUN wine-fix-shortcut.py /usr/share/applications/foobar2000.desktop

# Configure the container's exports
RUN <<'EOT' bash
	EXPORTS=(
		
		# Export the application shortcut for foobar2000
		foobar2000.desktop
		
	)
	
	# Resolve our exports and save the list
	echo "${EXPORTS[@]}" | save-exports.py
	
EOT

# Configure an init hook to symlink foobar2000's config directory to the host filesystem, so it persists across container restarts
RUN echo "wine-symlink-user-dir.py '.config/foobar2000' 'AppData/Roaming/foobar2000-v2'" >> /container-init-hooks.txt
