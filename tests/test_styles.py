import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_WORKSPACE,
)
from pytest import FixtureRequest

from geoserver import GeoServer

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
