from pathlib import Path
from typing import Generator, Optional

import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL
from pytest import FixtureRequest

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

TEST_DATA_DIR = Path(__file__).parent / "data"
# Names to reference the fixtures.
# Use these names to reference the fixtures in the tests.
TEST_WORKSPACE = "test_workspace"
TEST_DATA_STORE = "test_data_store"
TEST_FEATURE_TYPE = "test_feature_type"
TEST_COVERAGE_STORE = "test_coverage_store"
TEST_COVERAGE = "test_coverage"
TEST_GROUP = "test_group"
TEST_USER = "test_user"
TEST_ROLE = "test_role"


# Fixtures


@pytest.fixture(scope="module")
def test_workspace(test_geoserver: GeoServer) -> Generator[str, None, None]:
    workspace = "test-workspace"
    test_geoserver.create_workspace(body={"workspace": {"name": workspace}})
    yield workspace
    test_geoserver.delete_workspace(workspace, recurse=True)


@pytest.fixture(scope="module")
def test_data_store(test_geoserver: GeoServer, test_workspace: str) -> Generator[str, None, None]:
    file_path = Path(TEST_DATA_DIR, "vectors", "buildings.shp").resolve()
    data_store = "test-datastore"
    test_geoserver.upload_data_store(file_path, workspace=test_workspace, name=data_store, format="shp")
    yield data_store
    test_geoserver.delete_data_store(data_store, workspace=test_workspace, recurse=True)


@pytest.fixture(scope="module")
def test_feature_type(
    test_geoserver: GeoServer, test_workspace: str, test_data_store: str
) -> Generator[str, None, None]:
    data = test_geoserver.get_feature_type(test_data_store, workspace=test_workspace)
    yield data["featureType"]["name"]


@pytest.fixture(scope="module")
def test_coverage_store(test_geoserver: GeoServer, test_workspace: str) -> Generator[str, None, None]:
    coveragestore = "test-coveragestore"
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()
    assert file_path.exists()

    test_geoserver.upload_coverage_store(
        file=file_path,
        name=coveragestore,
        workspace=test_workspace,
        format="geotiff",
    )
    yield coveragestore
    test_geoserver.delete_coverage_store(coveragestore, workspace=test_workspace, recurse=True)


@pytest.fixture(scope="module")
def test_coverage(
    test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str
) -> Generator[str, None, None]:
    data = test_geoserver.get_coverage(test_coverage_store, workspace=test_workspace, store=test_coverage_store)
    yield data["coverage"]["name"]


@pytest.fixture(scope="module")
def test_group(test_geoserver: GeoServer) -> Generator[str, None, None]:
    name = "test-group"
    test_geoserver.create_user_group(name)
    yield name
    test_geoserver.delete_user_group(name)


@pytest.fixture(scope="module")
def test_user(test_geoserver: GeoServer) -> Generator[str, None, None]:
    username = "test-user"
    body = {
        "user": {
            "userName": username,
            "password": "test",
            "enabled": True,
        }
    }
    test_geoserver.create_user(body=body)
    yield username
    test_geoserver.delete_user(username)


@pytest.fixture(scope="module")
def test_role(test_geoserver: GeoServer) -> Generator[str, None, None]:
    name = "test-role"
    test_geoserver.create_role(name)
    yield name
    test_geoserver.delete_role(name)


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


# Coverages


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", [None, TEST_COVERAGE_STORE])
def test_get_coverages(
    test_geoserver: GeoServer, test_workspace: str, store: Optional[str], request: FixtureRequest
) -> None:
    if store == TEST_COVERAGE_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_coverages(workspace=test_workspace, store=store)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("coverage,store", [(TEST_COVERAGE_STORE, TEST_COVERAGE_STORE)])
def test_create_coverage(
    test_geoserver: GeoServer,
    test_workspace: str,
    coverage: str,
    store: str,
    request: FixtureRequest,
) -> None:
    if coverage == TEST_COVERAGE_STORE:
        coverage = request.getfixturevalue(coverage)
    if store == TEST_COVERAGE_STORE:
        store = request.getfixturevalue(store)

    body = test_geoserver.get_coverage(coverage, workspace=test_workspace, store=store)
    new_coverage = "tmp-coverage"
    body["coverage"]["name"] = new_coverage
    body["coverage"]["nativeName"] = new_coverage
    body["coverage"]["title"] = new_coverage
    body["coverage"]["keywords"]["string"] = [new_coverage, "WCS", "GeoTIFF"]
    body["coverage"]["metadata"]["entry"]["$"] = f"{new_coverage}_null"
    body["coverage"]["store"]["name"] = f"{test_workspace}:{new_coverage}"
    body["coverage"]["store"]["href"] = body["coverage"]["store"]["href"].replace(store, new_coverage)
    body["coverage"]["nativeCoverageName"] = new_coverage

    msg = test_geoserver.create_coverage(workspace=test_workspace, store=store, body=body)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", [TEST_COVERAGE_STORE, None])
def test_get_coverage(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_coverage_store: str,
    store: str,
    request: FixtureRequest,
) -> None:
    if store == TEST_COVERAGE_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_coverage(test_coverage_store, workspace=test_workspace, store=store)
    assert isinstance(data, dict)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_coverage("not-found", workspace=test_workspace)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_coverage(
    test_geoserver: GeoServer, test_workspace: str, test_coverage: str, test_coverage_store: str
) -> None:
    body = test_geoserver.get_coverage(test_coverage, workspace=test_workspace, store=test_coverage_store)
    description = "Coverage updated"
    body["coverage"]["description"] = description

    data = test_geoserver.update_coverage(
        test_coverage,
        workspace=test_workspace,
        store=test_coverage_store,
        body=body,
    )
    assert isinstance(data, str)

    body = test_geoserver.get_coverage(test_coverage, workspace=test_workspace, store=test_coverage_store)
    assert body["coverage"]["description"] == description


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_coverage(test_geoserver: GeoServer, test_workspace: str) -> None:
    coveragestore = "tmp-coveragestore"
    file_path = Path(TEST_DATA_DIR, "rasters", "raster.tif").resolve()
    test_geoserver.upload_coverage_store(
        file=file_path,
        name=coveragestore,
        workspace=test_workspace,
        format="geotiff",
    )

    msg = test_geoserver.delete_coverage(coveragestore, workspace=test_workspace, store=coveragestore, recurse=True)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_coverage(coveragestore, workspace=test_workspace, store=coveragestore)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset_coverage_caches(
    test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str, test_coverage: str
) -> None:
    msg = test_geoserver.reset_coverage_caches(test_coverage, workspace=test_workspace, store=test_coverage_store)
    assert isinstance(msg, str)


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


# Feature Types


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_feature_types(test_geoserver: GeoServer, test_workspace: str, test_data_store: str) -> None:
    data = test_geoserver.get_feature_types(workspace=test_workspace)
    assert isinstance(data, dict)

    data = test_geoserver.get_feature_types(workspace=test_workspace, store=test_data_store)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_feature_type(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", [None, TEST_DATA_STORE])
def test_get_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    store: Optional[str],
    request: FixtureRequest,
) -> None:
    if store == TEST_DATA_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=store)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("recalculate", [None, "", "nativebbox", "nativebbox,latlonbbox"])
def test_update_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
    recalculate: Optional[str],
) -> None:
    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert isinstance(data, dict)

    data["featureType"]["title"] = "Updated title"
    msg = test_geoserver.update_feature_type(
        test_feature_type,
        workspace=test_workspace,
        body=data,
        store=test_data_store,
        recalculate=recalculate,  # type: ignore[arg-type]
    )
    assert isinstance(msg, str)

    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert data["featureType"]["title"] == "Updated title"


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset_feature_type_caches(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
) -> None:
    msg = test_geoserver.reset_feature_type_caches(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
) -> None:
    msg = test_geoserver.delete_feature_type(
        test_feature_type,
        workspace=test_workspace,
        store=test_data_store,
        recurse=True,
    )
    assert isinstance(msg, str)


# Fonts


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_fonts(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_fonts()
    assert isinstance(data, dict)


# Layers


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace", [None, TEST_WORKSPACE])
def test_get_layers(test_geoserver: GeoServer, workspace: str) -> None:
    data = test_geoserver.get_layers(workspace=workspace)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace", [None, TEST_WORKSPACE])
def test_create_layer(test_geoserver: GeoServer, workspace: str) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace", [None, TEST_WORKSPACE])
def test_get_layer(test_geoserver: GeoServer, workspace: str, test_coverage: str, request: FixtureRequest) -> None:
    if workspace == TEST_WORKSPACE:
        workspace = request.getfixturevalue(workspace)

    data = test_geoserver.get_layer(test_coverage, workspace=workspace)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "layer,workspace",
    [
        (None, None),
        ("not-found", None),
        (TEST_COVERAGE_STORE, "not-found"),
        ("not-found", "not-found"),
    ],
)
def test_get_layer_invalid(test_geoserver: GeoServer, workspace: str, layer: str, request: FixtureRequest) -> None:
    if layer == TEST_COVERAGE_STORE:
        layer = request.getfixturevalue(layer)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_layer(layer, workspace=workspace)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_layer(test_geoserver: GeoServer, test_workspace: str, test_coverage: str) -> None:
    body = test_geoserver.get_layer(test_coverage)
    datestr = "2024-01-01 00:00:00.0 UTC"
    body["layer"]["dateCreated"] = datestr

    data = test_geoserver.update_layer(test_coverage, workspace=test_workspace, body=body)
    assert isinstance(data, str)

    body = test_geoserver.get_layer(test_coverage)
    assert body["layer"]["dateCreated"] == datestr


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_layer(test_geoserver: GeoServer, test_coverage: str) -> None:
    msg = test_geoserver.delete_layer(test_coverage)
    assert isinstance(msg, str)


# Layer Groups


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_layer_groups(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_layer_groups()
    assert isinstance(data, dict)

    data = test_geoserver.get_layer_groups(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_layer_group(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_layer_group(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_layer_group(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_layer_group(test_geoserver: GeoServer) -> None: ...


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


# Namespace


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_namespaces(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_namespaces()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_namespace(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_namespace(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_namespace(test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_namespace(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_namespace(test_geoserver: GeoServer) -> None: ...


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


# Reload, Reset


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset(test_geoserver: GeoServer) -> None:
    msg = test_geoserver.reset()
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reload(test_geoserver: GeoServer) -> None:
    msg = test_geoserver.reload()
    assert isinstance(msg, str)


# Resources


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_resource(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_resource(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_resource(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_head_resource(test_geoserver: GeoServer) -> None: ...


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


# Structured Coverages


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_coverage_granules(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_coverage_granule(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_coverage_granule(test_geoserver: GeoServer, test_workspace: str, test_coverage_store: str) -> None: ...


# Styles


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace", [None, TEST_WORKSPACE])
def test_get_styles(test_geoserver: GeoServer, workspace: str, request: FixtureRequest) -> None:
    if workspace == TEST_WORKSPACE:
        workspace = request.getfixturevalue(workspace)

    data = test_geoserver.get_styles(workspace=workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_style(test_geoserver: GeoServer, test_workspace: str) -> None:
    # file_path = Path(TEST_DATA_DIR, "styles", "elevation.sld").resolve()
    ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("style", ["generic", "line", "point", "polygon", "raster"])
def test_get_style(test_geoserver: GeoServer, style: str) -> None:
    data = test_geoserver.get_style(style)
    assert isinstance(data, dict)


# Templates


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "workspace,store",
    [
        (None, None),
        (TEST_WORKSPACE, None),
        (TEST_WORKSPACE, TEST_DATA_STORE),
    ],
)
def test_get_templates(test_geoserver: GeoServer, workspace: str, store: str, request: FixtureRequest) -> None:
    if workspace == TEST_WORKSPACE:
        workspace = request.getfixturevalue(workspace)
    if store == TEST_DATA_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_templates(workspace=workspace, store=store)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace,store", [(None, TEST_DATA_STORE)])
def test_get_templates_invalid(test_geoserver: GeoServer, workspace: str, store: str, request: FixtureRequest) -> None:
    if workspace == TEST_WORKSPACE:
        workspace = request.getfixturevalue(workspace)
    if store == TEST_DATA_STORE:
        store = request.getfixturevalue(store)

    with pytest.raises(ValueError):
        test_geoserver.get_templates(workspace=workspace, store=store)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_template(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_data_store: str,
    feature_type: str,
    test_coverage_store: str,
    coverage: str,
) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_insert_template(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_data_store: str,
    feature_type: str,
    test_coverage_store: str,
    coverage: str,
) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_template(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_data_store: str,
    feature_type: str,
    test_coverage_store: str,
    coverage: str,
) -> None: ...


# GeoServer XSLT transforms


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wfs_transforms(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_wfs_transform(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wfs_transform(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wfs_transform(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_wfs_transform(test_geoserver: GeoServer) -> None: ...


# WMS Layers


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wms_layers(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wms_layers(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_wms_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wms_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wms_layer(test_geoserver: GeoServer, test_workspace: str) -> None: ...


# WMS Stores


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wms_stores(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_wms_stores(workspace=test_workspace)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_wms_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_wms_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_wms_store(test_geoserver: GeoServer, test_workspace: str) -> None: ...


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


# Workspaces


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_workspaces(test_geoserver: GeoServer) -> None:
    data = test_geoserver.get_workspaces()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_workspace(test_geoserver: GeoServer) -> None:
    workspace = "tmp-workspace"
    body = {"workspace": {"name": workspace}}
    msg = test_geoserver.create_workspace(body=body)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.create_workspace(body=body)
    assert e_info.value.status_code == 409


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_workspace(test_geoserver: GeoServer, test_workspace: str) -> None:
    data = test_geoserver.get_workspace(test_workspace)
    assert isinstance(data, dict)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.get_workspace("not-found")
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("workspace", ["tmp-workspace"])
def test_delete_workspace(test_geoserver: GeoServer, workspace: str) -> None:
    msg = test_geoserver.delete_workspace(workspace)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_workspace(workspace)
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_workspace(test_geoserver: GeoServer, test_workspace: str) -> None:
    body = test_geoserver.get_workspace(test_workspace)
    name = "new-workspace"
    body["workspace"]["name"] = name

    msg = test_geoserver.update_workspace(test_workspace, body=body)
    assert isinstance(msg, str)

    body = test_geoserver.get_workspace(name)
    assert body["workspace"]["name"] == name

    # Revert
    body["workspace"]["name"] = test_workspace
    msg = test_geoserver.update_workspace(name, body=body)


# User Groups


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group",
    [
        (None, None),
        ("default", None),
        (None, TEST_GROUP),
    ],
)
def test_get_users(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)

    data = test_geoserver.get_users(service=service, group=group)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_users_invalid(test_geoserver: GeoServer) -> None:
    with pytest.raises(ValueError):
        test_geoserver.get_users(service="not-both", group="not-both")


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_create_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    body = {
        "user": {
            "userName": username,
            "password": "password",
            "enabled": True,
        }
    }

    msg = test_geoserver.create_user(body=body, service=service)
    assert isinstance(msg, str)


# Add parameters


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_update_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    data = test_geoserver.get_users()
    user = next((u for u in data["users"] if u["userName"] == username), None)
    assert user is not None

    user["enabled"] = False
    msg = test_geoserver.update_user(username, body={"user": user}, service=service)
    assert isinstance(msg, str)

    data = test_geoserver.get_users()
    user = next((u for u in data["users"] if u["userName"] == username), None)
    assert user["enabled"] is False


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("username,service", [("test", None), ("test2", "default")])
def test_delete_user(test_geoserver: GeoServer, username: str, service: Optional[str]) -> None:
    msg = test_geoserver.delete_user(username, service=service)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_user("not-found")
    assert e_info.value.status_code == 404


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_get_user_groups(test_geoserver: GeoServer, test_user: str, service: Optional[str]) -> None:
    data = test_geoserver.get_user_groups(user=test_user, service=service)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("group,service", [("tmp-group", None), ("tmp-group-default", "default")])
def test_create_group(test_geoserver: GeoServer, group: str, service: Optional[str]) -> None:
    msg = test_geoserver.create_user_group(group, service=service)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.create_user_group(group, service=service)
    status_code = e_info.value.status_code
    assert status_code >= 400 and status_code < 500


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_create_user_to_group(
    test_geoserver: GeoServer,
    test_user: str,
    test_group: str,
    service: Optional[str],
) -> None:
    msg = test_geoserver.associate_user(user=test_user, group=test_group, service=service)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("service", [None, "default"])
def test_delete_user_from_group(
    test_geoserver: GeoServer,
    test_user: str,
    test_group: str,
    service: Optional[str],
) -> None:
    msg = test_geoserver.disassociate_user(user=test_user, group=test_group, service=service)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("group,service", [("tmp-group", None), ("tmp-group-default", "default")])
def test_delete_group(test_geoserver: GeoServer, group: str, service: Optional[str]) -> None:
    msg = test_geoserver.delete_user_group(group, service=service)
    assert isinstance(msg, str)

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.delete_user_group(group, service=service)
    assert e_info.value.status_code == 404


# Roles


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group,user",
    [
        (None, None, None),
        ("default", None, None),
        (None, TEST_GROUP, None),
        ("default", TEST_GROUP, None),
        ("default", None, TEST_USER),
    ],
)
def test_get_roles(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    data = test_geoserver.get_roles(service=service, group=group, user=user)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "service,group,user",
    [
        (None, None, TEST_USER),
        (None, TEST_GROUP, TEST_USER),
        ("default", TEST_GROUP, TEST_USER),
    ],
)
def test_get_roles_invalid(
    test_geoserver: GeoServer,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.get_roles(service=service, user=user, group=group)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("role", ["tmp-role"])
def test_create_role(test_geoserver: GeoServer, role: str) -> None:
    msg = test_geoserver.create_role(role)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("role", ["tmp-role"])
def test_delete_role(test_geoserver: GeoServer, role: str) -> None:
    msg = test_geoserver.delete_role(role)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        ("role-service", "default", None, None),
        (TEST_ROLE, None, None, TEST_USER),
        (TEST_ROLE, "default", None, TEST_USER),
        (TEST_ROLE, None, TEST_GROUP, None),
        (TEST_ROLE, "default", TEST_GROUP, None),
    ],
)
def test_associate_role(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    msg = test_geoserver.associate_role(role=role, service=service, group=group, user=user)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        (TEST_ROLE, None, TEST_USER, TEST_GROUP),
        (TEST_ROLE, "default", TEST_USER, TEST_GROUP),
    ],
)
def test_associate_role_invalid(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.associate_role(role=role, user=user, group=group, service=service)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        ("role-service", "default", None, None),
        (TEST_ROLE, None, None, TEST_USER),
        (TEST_ROLE, "default", None, TEST_USER),
        (TEST_ROLE, None, TEST_GROUP, None),
        (TEST_ROLE, "default", TEST_GROUP, None),
    ],
)
def test_disassociate_role(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    msg = test_geoserver.disassociate_role(role=role, service=service, group=group, user=user)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize(
    "role,service,group,user",
    [
        (TEST_ROLE, None, TEST_USER, TEST_GROUP),
        (TEST_ROLE, "default", TEST_USER, TEST_GROUP),
    ],
)
def test_disassociate_role_invalid(
    test_geoserver: GeoServer,
    role: str,
    service: Optional[str],
    group: Optional[str],
    user: Optional[str],
    request: FixtureRequest,
) -> None:
    if role == TEST_ROLE:
        role = request.getfixturevalue(role)
    if group == TEST_GROUP:
        group = request.getfixturevalue(group)
    if user == TEST_USER:
        user = request.getfixturevalue(user)

    with pytest.raises(ValueError):
        test_geoserver.disassociate_role(role=role, user=user, group=group, service=service)
