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
from warnings import warn
from .enums import ReferenceTypes, PerceptionTypes

import importlib.util
visualization_available = importlib.util.find_spec("PyQt5") is not None and \
    importlib.util.find_spec("pyqtgraph") is not None

if visualization_available:
    try:
        import pyqtgraph
    except ImportError as e:
        warn(f'Disabled visualization since pyqtgraph could not be imported: {e}')
        visualization_available = False
    else:
        from . import visualization as vis

from ._version import get_versions_with_clean
__version__, __clean_version__ = [get_versions_with_clean()[v] for v in ['version', 'clean_version']]
del get_versions_with_clean
