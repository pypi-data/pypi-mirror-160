"""The converter module provides a service, that converts video files to h264.

While the system is running it explicitly does not convert the files in the current working folder
provided by the Watcher module.
"""

from sand.converter.pipeline.converter import Converter
