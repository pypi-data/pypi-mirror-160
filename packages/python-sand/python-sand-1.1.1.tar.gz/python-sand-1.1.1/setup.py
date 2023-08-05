# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sand',
 'sand.calibration',
 'sand.calibration.classes',
 'sand.calibration.helper',
 'sand.cli',
 'sand.config',
 'sand.converter',
 'sand.converter.pipeline',
 'sand.datatypes',
 'sand.definition',
 'sand.interfaces',
 'sand.interfaces.communication',
 'sand.interfaces.config',
 'sand.interfaces.shutdown',
 'sand.interfaces.synchronization',
 'sand.interfaces.util',
 'sand.logger',
 'sand.main',
 'sand.map',
 'sand.map.pipeline',
 'sand.metric',
 'sand.mqtt',
 'sand.neural',
 'sand.neural.pipeline',
 'sand.neural.third_party',
 'sand.neural.third_party.mlcvzoo',
 'sand.reader',
 'sand.reader.lidar',
 'sand.reader.lidar.pipeline',
 'sand.reader.video',
 'sand.recorder',
 'sand.recorder.lidar',
 'sand.recorder.lidar.pipeline',
 'sand.recorder.map',
 'sand.recorder.map.pipeline',
 'sand.recorder.video',
 'sand.recorder.video.pipeline',
 'sand.registry',
 'sand.sensor_fusion',
 'sand.sensor_fusion.pipeline',
 'sand.transformer',
 'sand.transformer.pipeline',
 'sand.util',
 'sand.view',
 'sand.view.frontend',
 'sand.view.stream',
 'sand.view.stream.pipeline',
 'sand.watcher',
 'sand.watcher.pipeline']

package_data = \
{'': ['*'],
 'sand.view.frontend': ['assets/css/*',
                        'assets/img/*',
                        'assets/js/*',
                        'static/*',
                        'template/*',
                        'template/parts/*']}

install_requires = \
['nptyping>=2.2.0,<3.0.0',
 'numpy>=1.21.4,<2.0.0',
 'opencv-contrib-python>=4.5,<4.6',
 'overrides>=6.1.0,<7.0.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'python-prctl>=1.8.1,<2.0.0',
 'yaml-config-builder>=6.0.0,<7.0.0']

extras_require = \
{'full': ['flask>=2.1.2,<3.0.0',
          'flask-socketio>=5.2.0,<6.0.0',
          'eventlet>=0.33.1,<0.34.0',
          'influxdb-client>=1.30.0,<2.0.0',
          'mlcvzoo-base>=3.2.1,<4.0.0',
          'mlcvzoo-mmdetection>=3.0.1,<4.0.0',
          'mlcvzoo-yolox>=4.0.2,<5.0.0'],
 'metric': ['influxdb-client>=1.30.0,<2.0.0'],
 'neural_base': ['mlcvzoo-base>=3.2.1,<4.0.0'],
 'neural_full': ['mlcvzoo-base>=3.2.1,<4.0.0',
                 'mlcvzoo-mmdetection>=3.0.1,<4.0.0',
                 'mlcvzoo-yolox>=4.0.2,<5.0.0'],
 'neural_mmdet': ['mlcvzoo-base>=3.2.1,<4.0.0',
                  'mlcvzoo-mmdetection>=3.0.1,<4.0.0'],
 'neural_yolox': ['mlcvzoo-base>=3.2.1,<4.0.0', 'mlcvzoo-yolox>=4.0.2,<5.0.0'],
 'publisher': ['flask>=2.1.2,<3.0.0',
               'flask-socketio>=5.2.0,<6.0.0',
               'eventlet>=0.33.1,<0.34.0']}

entry_points = \
{'console_scripts': ['generate_calibration_image = '
                     'sand.calibration.generate_calibration_image:main',
                     'image_calibration = '
                     'sand.calibration.image_calibration:main',
                     'image_downloader = sand.calibration.image_download:main',
                     'image_focal = sand.calibration.image_focal:main',
                     'map_calibration = sand.calibration.map_calibration:main',
                     'sand = sand.cli:run']}

setup_kwargs = {
    'name': 'python-sand',
    'version': '1.1.1',
    'description': 'Processing sensor and video data made easy',
    'long_description': '# Sensor and Neural Data Platform (SAND)\n\nThis project aims to make working with camera-streams (or video-streams in\ngeneral) easy, by providing an extensible framework to read, manipulate and\nrepublish images.\n\nIt was originally designed to manage an Object-Detection-System we setup on a\ntri-modal crane. The focus of this was to detect humans (and biomass in general)\nto make the processes at container-harbors safer in general.\n\nWhile developing we already recognized, that it could also be useful for generic\nusages, especially just recording some simple streams or do some light work,\nlike republishing streams.\n\n## How to setup\n\nIn general the installation process is quite simple. We described the simple\nterms here, but if you need a reference of some sort, we can recommend taking a\nlook at our [Dockerfile](build_container/Dockerfile) that we use for\nCI-purposes.\n\n### Prerequisites\n\n#### System Dependencies\n\nYou need those in any case:\n\n* gcc\n* build-essential\n* libcap-dev\n* python3-dev\n\n#### Neural Network\n\nIf you want to use a demo yolox please download the weights for YOLOX-X (trained\non the COCO dataset) from\n[here](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_x.pth)\nand either put them directly in `./config/detector_models/yolox/yolox_x_coco` or\nuse a symlink.\n\n### Development setup\n\nIf you only want to use SAND directly, you can skip this section. Although we\ncan very much recommend `poetry` in general for your own python projects.\n\nWe use `poetry` to manage our dependencies. To install `poetry` you can use\n[(more infos here)](https://python-poetry.org/docs/):\n```shell\n$ curl -sSL https://install.python-poetry.org | python -\n```\n\nOur dependencies are documented in the [pyproject.toml](pyproject.toml), the\nexplicit versions with hashes for the libraries you can find in\n[poetry.lock](poetry.lock).\n\nIn the following section you will see what different variants of the system we\nactually have.\n\n### Installation\n\nAttention: As "just" a user you probably don\'t want to install `poetry` or any\ndev-dependencies. Therefore you should always look at the `pip install` variant.\n\nWe have a couple of variants for the system, depending on what you want to do\nwith it. They can also be combined with each other if you want to use multiple\nfeatures. For development and especially unittesting you will need all extras:\n\n* neural\n    ```shell\n    $ poetry install --extras="neural"\n    $ pip install python-sand[neural]\n    ```\n    This installs all the dependencies that have something to do with machine\n    learning or neural networks. The main dependency here is the `MLCVZoo` which\n    provides us with an easy interface to work with inference and the results of\n    it in general. If you want to configure some kind of object-detection this\n    and the corresponding component in our system\n    ([NeuralNetwork](src/sand/neural/pipeline/neural.py)) are a good starting\n    point to look into.\n\n* metric\n    ```shell\n    $ poetry install --extras="metric"\n    $ pip install python-sand[metric]\n    ```\n    This concerns everything around an influx-db and metrics with a\n    grafana-dashboard. So if you want to monitor performance of basically\n    everything in our system you can start here. This absolutely needs a running\n    MQTT-Broker that the system can connect to. For development and "light"\n    running we have a mosquitto docker container setup in the\n    [docker-compose.yml](docker-compose.yml). `docker-compose` is also installed\n    via our `dev-dependencies` which get installed regardless of extras if you\n    install it via `poetry`. You will also need an influx-dbv2.\n    ```\n    $ docker-compose up -d mqtt influxdb grafana\n    ```\n\n* publisher\n    ```\n    $ poetry install --extras="publisher"\n    $ pip install python-sand[publisher]\n    ```\n    This basically gives you the tools to setup a basic flask server to deliver\n    in our case a static website where you can watch your streams in a basic\n    dashboard.\n\n### System\n\nIf you have installed `python-sand` in your environment it provides a couple of\nbinaries, that you can use to start different parts of the system.\n\n* `sand`\n\n    This is the main starter for the "normal" system. It has a couple of options\n    so be sure to take a look (via the normal `sand --help`)\n\n#### Long-term System\n\nIf you want to run install it on the actual system where it should run\nlong-term, we opted for a systemd-service to make starting/stopping very easy\nand also the logging gets easier. You probably still want to adapt it slightly\nto use your specific config or use additional links to match the default config\nname. You find the systemd file in this repository, it will not come bundled in\nthe python artifact.\n\nInstallation:\n```shell\n# cd /etc/systemd/system\n# ln -s /path/to/sand/sand.service .\n```\n\nAfter that you can start/stop it via:\n```shell\n# systemctl start sand\n```\n\nAlso the logs on the INFO-Level are routed through the journal, which is why you\ncan also read most of the logs via:\n```shell\n# journalctl -u sand\n```\n\n## FAQ\n\nMore like "We asked them ourselves at one point, and tried to find a spot where\nto save the knowledge".\n\n### How can you reset the admin password in grafana docker container?\n```shell\n$ docker exec CONTAINER_ID grafana-cli admin reset-admin-password admin\n```\n',
    'author': 'Moritz Sauter',
    'author_email': 'sauter@synyx.de',
    'maintainer': 'Moritz Sauter',
    'maintainer_email': 'sauter@synyx.de',
    'url': 'https://gitlab.com/sand7/sand',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
