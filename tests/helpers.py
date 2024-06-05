import os

import requests
from dotenv import load_dotenv

load_dotenv(".env", override=True)


def _service_running(url: str) -> bool:
    """Check if a service is running.

    Example:
        >>> _service_running("http://localhost:8080/geoserver")
        True
        >>> _service_running("http://localhost:1234/geoserver")
        False
    """
    try:
        response = requests.get(url)
        return response.ok
    except requests.ConnectionError:
        return False


GEOSERVER_HOST = os.getenv("GEOSERVER_HOST") or "localhost"
GEOSERVER_PORT = os.getenv("GEOSERVER_PORT") or "8080"
GEOSERVER_ADMIN_USER = os.getenv("GEOSERVER_ADMIN_USER") or "admin"
GEOSERVER_ADMIN_PASSWORD = os.getenv("GEOSERVER_ADMIN_PASSWORD") or "geoserver"
GEOSERVER_URL = f"http://{GEOSERVER_HOST}:{GEOSERVER_PORT}/geoserver"
GEOSERVER_RUNNING = _service_running(GEOSERVER_URL)
