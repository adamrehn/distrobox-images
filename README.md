# Container images for use with Distrobox

This repository contains Dockerfiles that produce container images suitable for use with [Distrobox](https://distrobox.it/). It is the modern successor to my older [**application-images**](https://github.com/adamrehn/application-images) and [**developer-images**](https://github.com/adamrehn/developer-images) repositories, which produced container images for use with my (now deprecated) [docker-shell](https://github.com/adamrehn/docker-shell) command-line tool.

The following container images are currently available:

- [**klogg**](./images/klogg/): encapsulates the [klogg](https://klogg.filimonov.dev/) log file viewer.

- [**swiss-army-knife**](./images/swiss-army-knife/): encapsulates a variety of command-line tools for development and productivity use.


## Using the pre-built images

All of the container images from this repository are available on Docker Hub. To use a pre-built image, run the command listed in the README for that image.


## Building the images

To build all of the container images, run the following command from the root of the repository:

```bash
./build.sh
```


## Legal

Copyright &copy; 2025, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](./LICENSE) for details.
