"""This module provides services that in general just 'watch' things and react on them.

The initial member is the :class:`DriveWatcher` which, you guessed it, watches the drives :)
It looks for the available memory on the different folders it gets via the :class:`config.DriveWatcherConfig` from
the :mod:`config`-module.
"""

from sand.watcher.pipeline.drive_watcher import DriveWatcher
