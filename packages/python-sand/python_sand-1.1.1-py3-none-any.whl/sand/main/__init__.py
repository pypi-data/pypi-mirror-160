"""Module to handle the graceful shutdown of the system.

It is called 'Main' because the main-method of this module, which is :meth:`main.Main.spin`, needs to be called on the
main thread of the system. As it registers signal handlers and wouldn't get those signals if its on any other thread
than the main one.
"""

from .main import Main
