from importlib.metadata import version as _version

from .geoserver import GeoServer
from .geowebcache import GeoWebCache

__version__ = _version("geoserver-py")
