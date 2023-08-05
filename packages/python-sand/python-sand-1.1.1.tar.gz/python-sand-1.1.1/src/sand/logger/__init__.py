"""Our adaptation of the default logger framework of python.

The two main reasons we did this were:
* We wanted to have two additional tags that were not really easily coverable by the default logging implementation:
** the class-name
** the function-/method-name
* Generally shorter function names like they are present in different other languages/systems like Android
"""

from .initialize import initialize_logger
from .logger import Logger
from .mqtt_logger import MQTTLoggerListener
