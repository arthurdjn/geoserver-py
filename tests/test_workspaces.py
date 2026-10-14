import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

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
