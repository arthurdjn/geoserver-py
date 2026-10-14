import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_DATA_STORE,
    TEST_WORKSPACE,
)
from pytest import FixtureRequest

from geoserver import GeoServer

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
