import os
import subprocess
from pathlib import Path
from typing import Generator

import pytest
from helpers import GEOSERVER_ADMIN_PASSWORD, GEOSERVER_ADMIN_USER, GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer, GeoWebCache


def pytest_configure(config: pytest.Config) -> None:
    # The tests skip themselves when GeoServer is down, which silently turns a broken CI setup into a green run.
    if os.getenv("GEOSERVER_REQUIRED") and not GEOSERVER_RUNNING:
        raise pytest.UsageError(f"GEOSERVER_REQUIRED is set but no GeoServer is running at {GEOSERVER_URL!r}.")


@pytest.fixture(scope="session", autouse=True)
def test_geoserver() -> Generator[GeoServer, None, None]:
    yield GeoServer(
        service_url=GEOSERVER_URL,
        username=GEOSERVER_ADMIN_USER,
        password=GEOSERVER_ADMIN_PASSWORD,
    )


@pytest.fixture(scope="session", autouse=True)
def test_geowebcache() -> Generator[GeoWebCache, None, None]:
    yield GeoWebCache(
        service_url=GEOSERVER_URL,
        username=GEOSERVER_ADMIN_USER,
        password=GEOSERVER_ADMIN_PASSWORD,
    )


@pytest.fixture(scope="session", autouse=True)
def test_postgis() -> Generator[None, None, None]:
    cmd = 'ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 user=admin dbname=db password=postgres" tests/data/vectors/landuse.shp -nlt PROMOTE_TO_MULTI -lco OVERWRITE=YES'
    subprocess.run(cmd, shell=True, check=False)
    yield None


# Catalog fixtures, created once per test module.


@pytest.fixture(scope="module")
def test_workspace(test_geoserver: GeoServer) -> Generator[str, None, None]:
    workspace = "test-workspace"
    test_geoserver.create_workspace(body={"workspace": {"name": workspace}})
    yield workspace
    test_geoserver.delete_workspace(workspace, recurse=True)


@pytest.fixture(scope="module")
def test_data_store(test_geoserver: GeoServer, test_workspace: str) -> Generator[str, None, None]:
    file_path = Path(Path(__file__).parent / "data", "vectors", "buildings.shp").resolve()
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
    file_path = Path(Path(__file__).parent / "data", "rasters", "raster.tif").resolve()
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
