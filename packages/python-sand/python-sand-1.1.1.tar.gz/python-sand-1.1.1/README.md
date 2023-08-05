# Sensor and Neural Data Platform (SAND)

This project aims to make working with camera-streams (or video-streams in
general) easy, by providing an extensible framework to read, manipulate and
republish images.

It was originally designed to manage an Object-Detection-System we setup on a
tri-modal crane. The focus of this was to detect humans (and biomass in general)
to make the processes at container-harbors safer in general.

While developing we already recognized, that it could also be useful for generic
usages, especially just recording some simple streams or do some light work,
like republishing streams.

## How to setup

In general the installation process is quite simple. We described the simple
terms here, but if you need a reference of some sort, we can recommend taking a
look at our [Dockerfile](build_container/Dockerfile) that we use for
CI-purposes.

### Prerequisites

#### System Dependencies

You need those in any case:

* gcc
* build-essential
* libcap-dev
* python3-dev

#### Neural Network

If you want to use a demo yolox please download the weights for YOLOX-X (trained
on the COCO dataset) from
[here](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_x.pth)
and either put them directly in `./config/detector_models/yolox/yolox_x_coco` or
use a symlink.

### Development setup

If you only want to use SAND directly, you can skip this section. Although we
can very much recommend `poetry` in general for your own python projects.

We use `poetry` to manage our dependencies. To install `poetry` you can use
[(more infos here)](https://python-poetry.org/docs/):
```shell
$ curl -sSL https://install.python-poetry.org | python -
```

Our dependencies are documented in the [pyproject.toml](pyproject.toml), the
explicit versions with hashes for the libraries you can find in
[poetry.lock](poetry.lock).

In the following section you will see what different variants of the system we
actually have.

### Installation

Attention: As "just" a user you probably don't want to install `poetry` or any
dev-dependencies. Therefore you should always look at the `pip install` variant.

We have a couple of variants for the system, depending on what you want to do
with it. They can also be combined with each other if you want to use multiple
features. For development and especially unittesting you will need all extras:

* neural
    ```shell
    $ poetry install --extras="neural"
    $ pip install python-sand[neural]
    ```
    This installs all the dependencies that have something to do with machine
    learning or neural networks. The main dependency here is the `MLCVZoo` which
    provides us with an easy interface to work with inference and the results of
    it in general. If you want to configure some kind of object-detection this
    and the corresponding component in our system
    ([NeuralNetwork](src/sand/neural/pipeline/neural.py)) are a good starting
    point to look into.

* metric
    ```shell
    $ poetry install --extras="metric"
    $ pip install python-sand[metric]
    ```
    This concerns everything around an influx-db and metrics with a
    grafana-dashboard. So if you want to monitor performance of basically
    everything in our system you can start here. This absolutely needs a running
    MQTT-Broker that the system can connect to. For development and "light"
    running we have a mosquitto docker container setup in the
    [docker-compose.yml](docker-compose.yml). `docker-compose` is also installed
    via our `dev-dependencies` which get installed regardless of extras if you
    install it via `poetry`. You will also need an influx-dbv2.
    ```
    $ docker-compose up -d mqtt influxdb grafana
    ```

* publisher
    ```
    $ poetry install --extras="publisher"
    $ pip install python-sand[publisher]
    ```
    This basically gives you the tools to setup a basic flask server to deliver
    in our case a static website where you can watch your streams in a basic
    dashboard.

### System

If you have installed `python-sand` in your environment it provides a couple of
binaries, that you can use to start different parts of the system.

* `sand`

    This is the main starter for the "normal" system. It has a couple of options
    so be sure to take a look (via the normal `sand --help`)

#### Long-term System

If you want to run install it on the actual system where it should run
long-term, we opted for a systemd-service to make starting/stopping very easy
and also the logging gets easier. You probably still want to adapt it slightly
to use your specific config or use additional links to match the default config
name. You find the systemd file in this repository, it will not come bundled in
the python artifact.

Installation:
```shell
# cd /etc/systemd/system
# ln -s /path/to/sand/sand.service .
```

After that you can start/stop it via:
```shell
# systemctl start sand
```

Also the logs on the INFO-Level are routed through the journal, which is why you
can also read most of the logs via:
```shell
# journalctl -u sand
```

## FAQ

More like "We asked them ourselves at one point, and tried to find a spot where
to save the knowledge".

### How can you reset the admin password in grafana docker container?
```shell
$ docker exec CONTAINER_ID grafana-cli admin reset-admin-password admin
```
