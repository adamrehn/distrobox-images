# foobar2000 Image

This container image encapsulates the [foobar2000](https://www.foobar2000.org/) audio player, running under Wine. The image bundles a number of foobar2000 components that provide support for additional audio formats.

To use the pre-built image from Docker Hub, run the following command:

```bash
# Create a Distrobox container using the Docker Hub version of
# the foobar2000 image, and export foobar2000 from the container
# for use on the host system
distrobox assemble create --file "https://distrobox-manifests.adamrehn.com/foobar2000.ini"
```

To use a locally-built version of the image, [build all of the container images in this repository](../../README.md#building-the-images) and then run the following command **from the root of the repository**:

```bash
# Create a Distrobox container using the local version of the
# foobar2000 image, and export foobar2000 from the container
# for use on the host system
distrobox assemble create --file 'manifests/foobar2000.ini'
```
