"""
.. include:: ./../README.md
"""
from .pydantic_utils import *

from .road import *
from .geometry import *
from .dynamics import *
from .weather import *

from .timestamps import Timestamps
from .reference_recording import ReferenceRecording
from .meta_data import MetaData
from .perception_recording import PerceptionRecording

from .settings import DefaultValues
from .reference_resolving import *

from .enums import ReferenceTypes, PerceptionTypes

import importlib.util
visualization_available = importlib.util.find_spec("PyQt5") is not None and \
    importlib.util.find_spec("pyqtgraph") is not None

if visualization_available:
    from . import visualization as vis


from ._version import get_versions
__version__ = get_versions()['version']
__clean_version__ = __version__.split('+')[0]
del get_versions
