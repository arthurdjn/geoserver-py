from pathlib import Path

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_DATA_DIR,
)

from geoserver import GeoServer

# Resources


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_resource(test_geoserver: GeoServer, test_workspace: str) -> None:
    path = f"data/{test_workspace}"
    data = test_geoserver.get_resource(path)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_head_resource(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_resource(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_resource(test_geoserver: GeoServer, test_workspace: str) -> None:
    coveragestore = "tmp-coveragestore"
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()
    test_geoserver.upload_coverage_store(
        file=file_path,
        name=coveragestore,
        workspace=test_workspace,
        format="geotiff",
    )
    path = f"data/{test_workspace}/{coveragestore}"
    msg = test_geoserver.delete_resource(path)
    assert isinstance(msg, str)
