# PE-Bear Image

This container image encapsulates the [PE-Bear](https://github.com/hasherezade/pe-bear) binary analysis tool for Windows [Portable Executable (PE)](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) files.

To use the pre-built image from Docker Hub, run the following command:

```bash
# Create a Distrobox container using the Docker Hub version of
# the PE-Bear image, and export PE-Bear from the container for use
# on the host system
distrobox assemble create --file "https://distrobox-manifests.adamrehn.com/pe-bear.ini"
```

To use a locally-built version of the image, [build all of the container images in this repository](../../README.md#building-the-images) and then run the following command **from the root of the repository**:

```bash
# Create a Distrobox container using the local version of the
# PE-Bear image, and export PE-Bear from the container for use on
# the host system
distrobox assemble create --file 'manifests/pe-bear.ini'
```
