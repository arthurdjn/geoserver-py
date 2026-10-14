import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_COVERAGE_STORE,
    TEST_WORKSPACE,
)
from pytest import FixtureRequest

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

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
