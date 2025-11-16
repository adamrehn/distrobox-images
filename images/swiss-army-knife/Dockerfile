FROM adamrehn/distrobox-base-arch:latest

# Install our various command-line tools, and cpanminus for installing ack
RUN --mount=type=cache,target=/var/cache/pacman,sharing=locked \
	pacman -Syu --needed --noconfirm \
		cpanminus \
		ffmpeg \
		gdal \
		git \
		graphviz \
		imagemagick \
		libsecret \
		pandoc-cli \
		pdf2svg \
		perl-image-exiftool \
		poppler \
		ripgrep

# Install ack
RUN /usr/bin/vendor_perl/cpanm --notest --install 'App::Ack'

# Add the directories containing ack and ExifTool to the PATH
ENV PATH="$PATH:/usr/bin/site_perl:/usr/bin/vendor_perl"

# Configure git to disable automatic line ending conversion
RUN git config --system core.autocrlf false

# Configure git to use the libsecret credential helper by default
RUN git config --system credential.helper /usr/lib/git-core/git-credential-libsecret

# Configure the container's exports
RUN <<'EOT' bash
	EXPORTS=(
		
		# Export the binaries for ack
		ack
		
		# Export the binaries for ExifTool
		exiftool
		
		# Export the binaries for FFmpeg
		ffmpeg
		ffplay
		ffprobe
		
		# Export the binaries for GDAL
		gdal
		gdal2tiles
		gdal2xyz
		gdal_calc
		gdal_contour
		gdal_create
		gdal_edit
		gdal_fillnodata
		gdal_footprint
		gdal_grid
		gdal_merge
		gdal_pansharpen
		gdal_polygonize
		gdal_proximity
		gdal_rasterize
		gdal_retile
		gdal_sieve
		gdal_translate
		gdal_viewshed
		gdaladdo
		gdalattachpct
		gdalbuildvrt
		gdalcompare
		gdaldem
		gdalenhance
		gdalinfo
		gdallocationinfo
		gdalmanage
		gdalmdiminfo
		gdalmdimtranslate
		gdalmove
		gdalsrsinfo
		gdaltindex
		gdaltransform
		gdalwarp
		gnmanalyse
		gnmmanage
		nearblack
		ogr2ogr
		ogr_layer_algebra
		ogrinfo
		ogrlineref
		ogrmerge
		ogrtindex
		pct2rgb
		rgb2pct
		sozip
		
		# Export the binaries for Git
		git
		
		# Export the binaries for Graphviz
		acyclic
		bcomps
		ccomps
		circo
		cluster
		diffimg
		dijkstra
		dot
		dot2gxl
		dot_builtins
		dot_sandbox
		edgepaint
		fdp
		gc
		gml2gv
		graphml2gv
		gv2gml
		gv2gxl
		gvcolor
		gvedit
		gvgen
		gvmap
		gvpack
		gvpr
		gxl2dot
		gxl2gv
		mm2gv
		neato
		nop
		osage
		patchwork
		prune
		sccmap
		sfdp
		tred
		twopi
		unflatten
		vimdot
		
		# Export the binaries for ImageMagick
		magick
		
		# Export the binaries for Pandoc
		pandoc
		
		# Export the binaries for pdf2svg
		pdf2svg
		
		# Export the binaries for Poppler
		pdfattach
		pdfdetach
		pdffonts
		pdfimages
		pdfinfo
		pdfseparate
		pdfsig
		pdftocairo
		pdftohtml
		pdftoppm
		pdftops
		pdftotext
		pdfunite
		
		# Export the binaries for ripgrep
		rg
		
	)
	
	# Resolve our exports and save the list
	echo "${EXPORTS[@]}" | save-exports.py
	
EOT
