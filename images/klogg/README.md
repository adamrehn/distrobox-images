# Klogg Image

This container image encapsulates the [klogg](https://klogg.filimonov.dev/) log file viewer.

To use the pre-built image from Docker Hub, run the following command:

```bash
# Create a Distrobox container using the Docker Hub version of
# the klogg image, and export klogg from the container for use
# on the host system
distrobox assemble create --file "https://distrobox-manifests.adamrehn.com/klogg.ini"
```

To use a locally-built version of the image, [build all of the container images in this repository](../../README.md#building-the-images) and then run the following command **from the root of the repository**:

```bash
# Create a Distrobox container using the local version of the
# klogg image, and export klogg from the container for use on
# the host system
distrobox assemble create --file 'manifests/klogg.ini'
```
