import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer

# Services (WMS, WFS, WCS, WMTS)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wms_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wms_settings()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wms_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    body = test_geoserver.get_wms_settings()

    body["wms"]["watermark"]["transparency"] = 75
    msg = test_geoserver.update_wms_settings(body=body)
    assert isinstance(msg, str)

    data = test_geoserver.get_wms_settings()
    assert data["wms"]["watermark"]["transparency"] == 75

    body["wms"]["watermark"]["transparency"] = 50
    msg = test_geoserver.update_wms_settings(body=body, workspace=test_workspace)
    assert isinstance(msg, str)

    data = test_geoserver.get_wms_settings(workspace=test_workspace)
    assert data["wms"]["watermark"]["transparency"] == 50


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_wms_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    msg = test_geoserver.delete_wms_settings(workspace=test_workspace)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wfs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wfs_settings()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wfs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    body = test_geoserver.get_wfs_settings()

    body["wfs"]["maxFeatures"] = 900_000
    msg = test_geoserver.update_wfs_settings(body=body)
    assert isinstance(msg, str)

    data = test_geoserver.get_wfs_settings()
    assert data["wfs"]["maxFeatures"] == 900_000

    body["wfs"]["maxFeatures"] = 800_000
    msg = test_geoserver.update_wfs_settings(body=body, workspace=test_workspace)
    assert isinstance(msg, str)

    data = test_geoserver.get_wfs_settings(workspace=test_workspace)
    assert data["wfs"]["maxFeatures"] == 800_000


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_wfs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    msg = test_geoserver.delete_wfs_settings(workspace=test_workspace)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wcs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wms_settings()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wcs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    body = test_geoserver.get_wcs_settings()

    body["wcs"]["defaultDeflateCompressionLevel"] = 8
    msg = test_geoserver.update_wcs_settings(body=body)
    assert isinstance(msg, str)

    data = test_geoserver.get_wcs_settings()
    assert data["wcs"]["defaultDeflateCompressionLevel"] == 8

    body["wcs"]["defaultDeflateCompressionLevel"] = 7
    msg = test_geoserver.update_wcs_settings(body=body, workspace=test_workspace)
    assert isinstance(msg, str)

    data = test_geoserver.get_wcs_settings(workspace=test_workspace)
    assert data["wcs"]["defaultDeflateCompressionLevel"] == 7


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_wcs_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    msg = test_geoserver.delete_wcs_settings(workspace=test_workspace)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wmts_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wmts_settings()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wmts_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    body = test_geoserver.get_wmts_settings()

    body["wmts"]["abstrct"] = "Updated abstract."
    msg = test_geoserver.update_wmts_settings(body=body)
    assert isinstance(msg, str)

    data = test_geoserver.get_wmts_settings()
    assert data["wmts"]["abstrct"] == "Updated abstract."

    body["wmts"]["abstrct"] = "Updated abstract 2."
    msg = test_geoserver.update_wmts_settings(body=body, workspace=test_workspace)
    assert isinstance(msg, str)

    data = test_geoserver.get_wmts_settings(workspace=test_workspace)
    assert data["wmts"]["abstrct"] == "Updated abstract 2."


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_wmts_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    msg = test_geoserver.delete_wmts_settings(workspace=test_workspace)
    assert isinstance(msg, str)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_oseo_settings(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_oseo_settings()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_oseo_settings(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_oseo_settings(test_geoserver: GeoServer) -> None: ...


# Settings


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_settings(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_settings()
    assert isinstance(data, dict)

    data = test_geoserver.get_settings(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_settings(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_settings(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_settings(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_contact_settings(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_contact_settings()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_contact_settings(test_geoserver: GeoServer) -> None: ...
