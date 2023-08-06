Copyright 2020 Unlimited Robotics

# Unlimited Robotics SDK

## Components versions:

- Ra-Ya Simulator `1.0.3`
- Ra-Ya OS `1.0.4`
- Ra-Ya Python Library `2.8.12`
- Ra-Ya Simulation Workspace `1.0.6`
- GGS

## Usage

``` bash
$ rayasdk [-h] [-v | -q] command {command-options}
```

Optional arguments:
* `-h`, `--help`: show this help message and exit.
* `-v`, `--verbose`: increase output verbosity.
* `-q`, `--quiet`: don't print on stdout.

Positional arguments:

* `command`: SDK Command

Commands:

* `simulator`: runs the simulator and the bringup.
* `init`: initialize Raya project in current folder.
* `scan`: discover robots in the local network.
* `connect`: connect current raya proyect to a robot or simulator.
* `run`: execute current Raya project.
* `kill`: kill all the Ra-Ya related containers.

## Docker container

All the Ra-Ya related stuff is execute inside the Ra-Ya container. It includes:

* Ra-Ya bringup (including the bridge)
* Robots scanner
* Applications

Thanks to this, the developer doesn't need to install anything in their computer.

Each time the `rakasdk` is executed, it verifies the existence of the image (see method `check_container` in the file [docker_handler.py](/rayasdk/container_handlers/docker_handler.py)). It checks the image tag acording to the constants in the file [constants.py](/rayasdk/constants.py):

Image tag format: 

```
{RAYAENV_DOCKER_IMGNAME}:{RAYAENV_DOCKER_VERSION}
```

For example, when `RAYAENV_DOCKER_IMGNAME=raya_os` and `RAYAENV_DOCKER_VERSION=0.5.0`, it looks for the image:

```
raya_os:0.5.0
```

If it doesn't find the image, it download it as a `tar.gz` file from the link `RAYAENV_DOCKER_URL` and match its sha256 checksum with the one in `RAYAENV_DOCKER_SHA256`. Then, it stores the image in a temporal folder (`RAYAENV_DOCKER_IMGPATH`) and load it in the docker system. After that, the image is ready for future uses.

## Commands

## `simulator`

This command checks for the existence of the simulator in the path `SIM_PATH`. (looks for the version `GARYSIM_VERSION`). If it doens't find it, it's downloaded from `GARYSIM_URL` and checked with the sha256 checksum `GARYSIM_SHA256`.

If the simulator is avaiable, it launch it, and also launches the ra-ya bringup in a new container named:

```
{RAYAENV_DOCKER_CONTAINERPREFIX}_simbridge
```

## `init`

Initialize Raya project in current folder.

Usage: 

``` bash
$ rayasdk init [-h] --app-id APP_ID [--app-name APP_NAME]
```

Required arguments:
* `--app-id APP_ID`: application unique identificator

Optional arguments:
* `--app-name APP_NAME`: application name
* `-h`, `--help`: show this help message and exit

Example:

``` bash
$ urdsk init --app-id helloworld --app-name 'Hello World'
```

## `scan`

Discover robots in the local network.

Usage:

``` bash
$ rayasdk scan [-h]
```

Optional arguments:

* `-h`, `--help`: show this help message and exit.

Example:

``` bash
$ rayasdk scan
```

Output:

```
Scanning local network for robots...

Robot ID        IP Address       DDS Channel
--------------  -------------  -------------
GARY_KITCHEN    193.168.20.36              3
GARY_2665232    193.168.20.76              1
GARY_RECEPTION  193.168.20.12              2
```

The scanner runs in a new container named:

```
{RAYAENV_DOCKER_CONTAINERPREFIX}_scanner
```

## `connect`

Connect current raya proyect to a robot or simulator.

Usage:

``` bash
usage: rayasdk connect [--robot-id ROBOT_ID | --simulator]
```

Required mutually exclusive arguments:

* `--robot-id ROBOT_ID`: robot identificator (from scan list).
* `--simulator`: connect the project to the simulator.

Optional arguments:

* `-h`, `--help`: show this help message and exit.

## `run`

Execute current Raya project.

Usage:

``` bash
usage: rayasdk run [--local]
```

Optional arguments:

* `--local`: executes the application inside the robot.
* `-h`, `--help`: show this help message and exit.

The applications runs in a new container named:

```
{RAYAENV_DOCKER_CONTAINERPREFIX}_<app_id>
```
