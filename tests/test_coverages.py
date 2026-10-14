from pathlib import Path
from typing import Optional

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_COVERAGE_STORE,
    TEST_DATA_DIR,
)
from pytest import FixtureRequest

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

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
