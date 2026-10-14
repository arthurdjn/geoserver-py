from pathlib import Path
from typing import Callable, Generator

import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer

TEST_DATA_DIR = Path(__file__).parent / "data"
WORKSPACE = "test-exists"

pytestmark = pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")


@pytest.fixture(scope="module", autouse=True)
def catalog(test_geoserver: GeoServer) -> Generator[None, None, None]:
    """A workspace with a coverage store, a data store and a cascaded WMS store."""
    if test_geoserver.workspace_exists(WORKSPACE):
        test_geoserver.delete_workspace(WORKSPACE, recurse=True)
    test_geoserver.create_workspace_from_name(WORKSPACE)
    # A GeoTIFF upload names the coverage and the layer after the store.
    test_geoserver.upload_coverage_store(
        TEST_DATA_DIR / "rasters" / "raster.tif", workspace=WORKSPACE, name="raster", format="geotiff"
    )
    test_geoserver.upload_data_store(TEST_DATA_DIR / "vectors" / "buildings.shp", workspace=WORKSPACE, name="vectors")
    # Cascade the WMS of the same GeoServer, as seen from its own container.
    capabilities = "http://localhost:8080/geoserver/wms?SERVICE=WMS&REQUEST=GetCapabilities"
    test_geoserver.create_wms_store({"wmsStore": {"name": "wms", "capabilitiesURL": capabilities}}, workspace=WORKSPACE)
    test_geoserver.create_wms_layer(
        {"wmsLayer": {"name": "cascaded", "nativeName": f"{WORKSPACE}:raster"}}, workspace=WORKSPACE, store="wms"
    )
    yield
    test_geoserver.delete_workspace(WORKSPACE, recurse=True)


@pytest.mark.parametrize(
    "exists",
    [
        pytest.param(lambda gs, name: gs.coverage_store_exists(name, workspace=WORKSPACE), id="coverage_store"),
        pytest.param(lambda gs, name: gs.coverage_exists(name, workspace=WORKSPACE), id="coverage"),
        pytest.param(
            lambda gs, name: gs.coverage_exists(name, workspace=WORKSPACE, store="raster"), id="coverage+store"
        ),
        pytest.param(lambda gs, name: gs.layer_exists(name, workspace=WORKSPACE), id="layer"),
        pytest.param(lambda gs, name: gs.layer_exists(f"{WORKSPACE}:{name}"), id="layer+qualified"),
    ],
)
def test_raster_exists(test_geoserver: GeoServer, exists: Callable[[GeoServer, str], bool]) -> None:
    assert exists(test_geoserver, "raster") is True
    assert exists(test_geoserver, "missing") is False


@pytest.mark.parametrize("store", [None, "vectors"])
def test_feature_type_exists(test_geoserver: GeoServer, store: str) -> None:
    feature_types = test_geoserver.get_feature_types(workspace=WORKSPACE, store="vectors")
    name = feature_types["featureTypes"]["featureType"][0]["name"]

    assert test_geoserver.feature_type_exists(name, workspace=WORKSPACE, store=store) is True
    assert test_geoserver.feature_type_exists("missing", workspace=WORKSPACE, store=store) is False


def test_namespace_exists(test_geoserver: GeoServer) -> None:
    assert test_geoserver.namespace_exists(WORKSPACE) is True
    assert test_geoserver.namespace_exists("missing") is False


def test_wms_store_exists(test_geoserver: GeoServer) -> None:
    assert test_geoserver.wms_store_exists("wms", workspace=WORKSPACE) is True
    assert test_geoserver.wms_store_exists("missing", workspace=WORKSPACE) is False


@pytest.mark.parametrize("store", [None, "wms"])
def test_wms_layer_exists(test_geoserver: GeoServer, store: str) -> None:
    assert test_geoserver.wms_layer_exists("cascaded", workspace=WORKSPACE, store=store) is True
    assert test_geoserver.wms_layer_exists("missing", workspace=WORKSPACE, store=store) is False


def test_coveragestore_exists_is_deprecated(test_geoserver: GeoServer) -> None:
    with pytest.deprecated_call():
        assert test_geoserver.coveragestore_exists("raster", workspace=WORKSPACE) is True
