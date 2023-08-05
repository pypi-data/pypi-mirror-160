"""Data class for storing information that is needed to classify an object instance"""

from typing import NamedTuple


class ClassIdentifier(NamedTuple):
    class_id: int
    class_name: str
