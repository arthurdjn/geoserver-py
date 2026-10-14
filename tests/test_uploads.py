import zipfile
from pathlib import Path
from typing import Generator

import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

TEST_DATA_DIR = Path(__file__).parent / "data"
RASTER = TEST_DATA_DIR / "rasters" / "raster.tif"

pytestmark = pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")


@pytest.fixture(scope="module")
def workspace(test_geoserver: GeoServer) -> Generator[str, None, None]:
    name = "test-uploads"
    if test_geoserver.workspace_exists(name):
        test_geoserver.delete_workspace(name, recurse=True)
    test_geoserver.create_workspace_from_name(name)
    yield name
    test_geoserver.delete_workspace(name, recurse=True)


@pytest.fixture
def mosaic(test_geoserver: GeoServer, workspace: str, tmp_path: Path) -> Generator[str, None, None]:
    """An image mosaic with a single granule, indexed in a shapefile."""
    archive = tmp_path / "mosaic.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(RASTER, arcname="granule_1.tif")

    name = "test-mosaic"
    test_geoserver.upload_coverage_store(archive, workspace=workspace, name=name, format="imagemosaic")
    yield name
    test_geoserver.delete_coverage_store(name, workspace=workspace, recurse=True)


def granule_locations(geoserver: GeoServer, workspace: str, store: str) -> list:
    coverage = geoserver.get_coverages(workspace=workspace, store=store)["coverages"]["coverage"][0]["name"]
    granules = geoserver.get_coverage_granules(coverage, workspace=workspace, store=store)
    return sorted(feature["properties"]["location"] for feature in granules["features"])


def test_upload_coverage_store_from_file_object(test_geoserver: GeoServer, workspace: str) -> None:
    with open(RASTER, "rb") as f:
        test_geoserver.upload_coverage_store(f, workspace=workspace, name="raster-from-file-object", format="geotiff")

    store = test_geoserver.get_coverage_store("raster-from-file-object", workspace=workspace)
    assert store["coverageStore"]["name"] == "raster-from-file-object"


def test_upload_data_store_from_file_object(test_geoserver: GeoServer, workspace: str) -> None:
    with open(TEST_DATA_DIR / "vectors" / "buildings.zip", "rb") as f:
        test_geoserver.upload_data_store(f, workspace=workspace, name="vector-from-file-object")

    assert test_geoserver.data_store_exists("vector-from-file-object", workspace=workspace)


def test_upload_style_from_file_object(test_geoserver: GeoServer, workspace: str) -> None:
    with open(TEST_DATA_DIR / "styles" / "elevation.sld", "rb") as f:
        test_geoserver.upload_style(f, name="style-from-file-object", workspace=workspace)

    sld = test_geoserver.download_style("style-from-file-object", workspace=workspace)
    assert "StyledLayerDescriptor" in sld


def test_upload_coverage_store_coverage_name(test_geoserver: GeoServer, workspace: str) -> None:
    test_geoserver.upload_coverage_store(
        RASTER, workspace=workspace, name="named-coverage", format="geotiff", coverage_name="custom_name"
    )

    coverages = test_geoserver.get_coverages(workspace=workspace, store="named-coverage")
    assert [coverage["name"] for coverage in coverages["coverages"]["coverage"]] == ["custom_name"]


def test_upload_coverage_store_unknown_format(test_geoserver: GeoServer, workspace: str) -> None:
    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.upload_coverage_store(RASTER, workspace=workspace, name="unknown-format", format="foo")

    # The error message lists the formats the server accepts.
    assert e_info.value.status_code == 400
    assert "geotiff" in e_info.value.message


def test_upload_coverage_store_does_not_harvest(
    test_geoserver: GeoServer, workspace: str, mosaic: str, tmp_path: Path
) -> None:
    archive = tmp_path / "granules.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(RASTER, arcname="granule_2.tif")

    # Uploading to an existing mosaic does not add the granules to its index (#22).
    test_geoserver.upload_coverage_store(archive, workspace=workspace, name=mosaic, format="imagemosaic")
    assert granule_locations(test_geoserver, workspace, mosaic) == ["granule_1.tif"]


def test_harvest_coverage_store_file(test_geoserver: GeoServer, workspace: str, mosaic: str) -> None:
    msg = test_geoserver.harvest_coverage_store(RASTER, workspace=workspace, name=mosaic, filename="granule_2.tif")

    assert isinstance(msg, str)
    assert granule_locations(test_geoserver, workspace, mosaic) == ["granule_1.tif", "granule_2.tif"]


def test_harvest_coverage_store_file_object(test_geoserver: GeoServer, workspace: str, mosaic: str) -> None:
    with open(RASTER, "rb") as f:
        test_geoserver.harvest_coverage_store(f, workspace=workspace, name=mosaic)

    assert granule_locations(test_geoserver, workspace, mosaic) == ["granule_1.tif", "raster.tif"]


def test_harvest_coverage_store_zip(test_geoserver: GeoServer, workspace: str, mosaic: str, tmp_path: Path) -> None:
    archive = tmp_path / "granules.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(RASTER, arcname="granule_2.tif")
        zf.write(RASTER, arcname="granule_3.tif")

    test_geoserver.harvest_coverage_store(archive, workspace=workspace, name=mosaic)

    assert granule_locations(test_geoserver, workspace, mosaic) == ["granule_1.tif", "granule_2.tif", "granule_3.tif"]


def test_harvest_coverage_store_not_structured(test_geoserver: GeoServer, workspace: str) -> None:
    test_geoserver.upload_coverage_store(RASTER, workspace=workspace, name="single-geotiff", format="geotiff")

    with pytest.raises(GeoServerError) as e_info:
        test_geoserver.harvest_coverage_store(RASTER, workspace=workspace, name="single-geotiff", format="geotiff")
    assert e_info.value.status_code == 405
