from pathlib import Path

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_DATA_DIR,
)

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

# Coverage Stores


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_coverage_stores(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_coverage_stores(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_coverage_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()
    body = {
        "coverageStore": {
            "name": f"{file_path.stem}-store1",
            "workspace": test_workspace,
            "enabled": True,
            "type": "GeoTIFF",
            "__default": True,
        }
    }

    msg = test_geoserver.create_coverage_store(workspace=test_workspace, body=body)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_upload_coverage_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()
    data = test_geoserver.upload_coverage_store(
        file=file_path,
        workspace=test_workspace,
        name=f"{file_path.stem}-store2",
        format="geotiff",
    )
    assert isinstance(data, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_coverage_store(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None:
    data = test_geoserver.get_coverage_store(test_coverage_store, workspace=test_workspace)
    assert isinstance(data, dict)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_coverage_store("not-found", workspace=test_workspace)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_coverage_store(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None:
    body = test_geoserver.get_coverage_store(test_coverage_store, workspace=test_workspace)
    datestr = "2024-01-01 00:00:00.0 UTC"
    body["coverageStore"]["dateModified"] = datestr

    data = test_geoserver.update_coverage_store(test_coverage_store, workspace=test_workspace, body=body)
    assert isinstance(data, str)

    body = test_geoserver.get_coverage_store(test_coverage_store, workspace=test_workspace)
    assert body["coverageStore"]["dateModified"] == datestr


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_coverage_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()

    _ = test_geoserver.upload_coverage_store(
        file=file_path,
        workspace=test_workspace,
        name=f"{file_path.stem}-store3",
        format="geotiff",
    )

    msg = test_geoserver.delete_coverage_store(f"{file_path.stem}-store3", workspace=test_workspace, recurse=True)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_coverage_store(f"{file_path.stem}-store3", workspace=test_workspace, recurse=True)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset_coverage_store_caches(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None:
    msg = test_geoserver.reset_coverage_store_caches(test_coverage_store, workspace=test_workspace)
    assert isinstance(msg, str)
