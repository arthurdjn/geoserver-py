import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer

# WMTS Layers


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wmts_layers(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wms_layers(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_wmts_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wmts_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wmts_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


# WMTS Stores


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wmts_stores(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wmts_stores(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_wmts_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wmts_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wmts_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...
