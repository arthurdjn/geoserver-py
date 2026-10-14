import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer

# About


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_manifest(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_manifest()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_version(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_version()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_status(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_status()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_system_status(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_system_status()
    assert isinstance(data, dict)


# Fonts


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_fonts(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_fonts()
    assert isinstance(data, dict)


# Logging


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_logging(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_logging()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_logging(test_geoserver: GeoServer) -> None:
    body = test_geoserver.get_logging()
    std_out_logging = not body["logging"]["stdOutLogging"]
    body["logging"]["stdOutLogging"] = std_out_logging

    data = test_geoserver.update_logging(body=body)
    assert isinstance(data, str)

    body = test_geoserver.get_logging()
    assert body["logging"]["stdOutLogging"] == std_out_logging


# Monitoring


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_monitored_requests(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_monitored_requests()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_monitored_request(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_monitored_requests()
    request_list = data["org.geoserver.monitor.RequestDatas"]["org.geoserver.monitor.RequestData"]
    assert isinstance(request_list, list) and len(request_list) > 0

    request_id = request_list[0]["name"]
    data = test_geoserver.get_monitored_request(request_id)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_monitored_requests(test_geoserver: GeoServer) -> None:
    msg = test_geoserver.delete_monitored_requests()
    assert isinstance(msg, str)


# Reload, Reset


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset(test_geoserver: GeoServer) -> None:
    msg = test_geoserver.reset()
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reload(test_geoserver: GeoServer) -> None:
    msg = test_geoserver.reload()
    assert isinstance(msg, str)
