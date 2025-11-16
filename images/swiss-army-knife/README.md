# Swiss Army Knife Image

This container image encapsulates a variety of command-line tools for development and productivity use. The following tools are currently included:

- [ack](https://beyondgrep.com/)
- [ExifTool](https://exiftool.org/)
- [FFmpeg](https://www.ffmpeg.org/)
- [GDAL](https://gdal.org/)
- [Git](https://git-scm.com/)
- [Graphviz](https://www.graphviz.org/)
- [ImageMagick](https://imagemagick.org/index.php)
- [Pandoc](https://pandoc.org/)
- [pdf2svg](https://github.com/dawbarton/pdf2svg)
- [Poppler utilities](https://poppler.freedesktop.org/)
- [ripgrep](https://github.com/BurntSushi/ripgrep)

To get started using the image, [build all of the container images in this repository](../../README.md#building-the-images) and then run the following commands:

```bash
# Create a Distrobox container using the Swiss Army Knife image
distrobox create --name 'swiss-army-knife' --image 'adamrehn/distrobox-swiss-army-knife:latest'

# Export the binaries from the container for use from the host system
distrobox enter 'swiss-army-knife' -- apply-exports.py
```
