import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer

# Security


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_master_password(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_master_password()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_master_password(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_password(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_master_password()
    password = data["oldMasterPassword"]
    body = {
        "oldPassword": password,
        "newPassword": password,
    }

    msg = test_geoserver.update_password(body=body)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_catalog_mode(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_catalog_mode()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def get_catalog_mode(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_catalog_mode()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_catalog_mode(test_geoserver: GeoServer) -> None:
    mode = "MIXED"
    body = {"mode": mode}

    msg = test_geoserver.update_catalog_mode(body=body)
    assert isinstance(msg, str)

    body = test_geoserver.get_catalog_mode()
    assert body["mode"] == mode


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_security_layers(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_security_layers()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_security_layer(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_security_layer(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_security_services(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_security_services()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_security_services(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_security_access(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_security_access()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_security_access(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_security_access(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_security_access(test_geoserver: GeoServer) -> None: ...
