from pathlib import Path

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_DATA_DIR,
    TEST_DATA_STORE,
)
from pytest import FixtureRequest

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

# Data Stores


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_data_stores(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_data_stores(workspace=test_workspace)
    assert isinstance(data, dict)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_workspace("not-found")
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_data_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    file_path = Path(TEST_DATA_DIR, "vectors", "buildings.shp").resolve()
    body = {
        "dataStore": {
            "name": file_path.stem,
            "connectionParameters": {
                "entry": [
                    {"@key": "url", "$": f"file:{file_path.as_posix()}"},
                    {"@key": "filetype", "$": "shapefile"},
                ]
            },
        }
    }

    msg = test_geoserver.create_data_store(workspace=test_workspace, body=body)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.create_data_store(workspace=test_workspace, body=body)
    assert e_info.value.status_code == 500

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.create_data_store(workspace="not-found", body=body)
    assert e_info.value.status_code == 500


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_upload_data_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    file_path = Path(TEST_DATA_DIR, "vectors", "buildings.shp").resolve()
    msg = test_geoserver.upload_data_store(workspace=test_workspace, file=file_path, format="shp")
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", ["buildings", TEST_DATA_STORE])
def test_get_data_store(test_geoserver: GeoServer, test_workspace: str, store: str, request: FixtureRequest) -> None:
    if store == TEST_DATA_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_data_store(store, workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", [None, "not-found"])
def test_get_data_store_invalid(test_geoserver: GeoServer, test_workspace: str, store: str) -> None:
    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_data_store(store, workspace=test_workspace)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_data_store(test_geoserver: GeoServer, test_workspace: str) -> None:
    data_store = "tmp-datastore"
    file_path = Path(TEST_DATA_DIR, "vectors", "buildings.shp").resolve()
    body = {
        "dataStore": {
            "name": data_store,
            "connectionParameters": {
                "entry": [
                    {"@key": "url", "$": f"file:{file_path.as_posix()}"},
                    {"@key": "filetype", "$": "shapefile"},
                ]
            },
        }
    }

    msg = test_geoserver.create_data_store(workspace=test_workspace, body=body)
    assert isinstance(msg, str)

    msg = test_geoserver.delete_data_store(data_store, workspace=test_workspace)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_data_store(data_store, workspace=test_workspace)
    assert e_info.value.status_code == 404

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_data_store(data_store, workspace="not-found")
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_data_store(test_geoserver: GeoServer, test_workspace: str, test_data_store: str) -> None:
    body = test_geoserver.get_data_store(test_data_store, workspace=test_workspace)
    datestr = "2024-01-01 00:00:00.0 UTC"
    body["dataStore"]["dateCreated"] = datestr

    data = test_geoserver.update_data_store(test_data_store, workspace=test_workspace, body=body)
    assert isinstance(data, str)

    body = test_geoserver.get_data_store(test_data_store, workspace=test_workspace)
    assert body["dataStore"]["dateCreated"] == datestr


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset_data_store_caches(test_geoserver: GeoServer, test_workspace: str, test_data_store: str) -> None:
    msg = test_geoserver.reset_data_store_caches(test_data_store, workspace=test_workspace)
    assert isinstance(msg, str)
