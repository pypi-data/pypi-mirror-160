"""This module contains the definitions for different classes that are shared throughout the system.

The main thing here are :class:`SandNode` which provides our general thread handling and logging mechanisms and already
implements a sensible default for our shutdown system.
Another very notable member of this module which is already used by the :class:`SandNode` is the :class:`ShutdownAble`
which sets up the basic interface for a graceful shutdown and probably more importantly also registers the node in the
:mod:`registry`-module.

Generally the different interfaces are also shared between the modules and not specific to one. That is why they are
here.
"""
