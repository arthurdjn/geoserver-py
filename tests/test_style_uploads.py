import io
import zipfile
from pathlib import Path
from typing import Generator

import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer
from geoserver.exceptions import GeoServerError

SLD_PATH = Path(__file__).parent / "data" / "styles" / "elevation.sld"
WORKSPACE = "test-style-uploads"

pytestmark = pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")


@pytest.fixture(scope="module", autouse=True)
def workspace(test_geoserver: GeoServer) -> Generator[None, None, None]:
    if test_geoserver.workspace_exists(WORKSPACE):
        test_geoserver.delete_workspace(WORKSPACE, recurse=True)
    test_geoserver.create_workspace_from_name(WORKSPACE)
    yield
    test_geoserver.delete_workspace(WORKSPACE, recurse=True)


def sld(label: str = "label") -> str:
    return SLD_PATH.read_text(encoding="utf-8").replace('label="label"', f'label="{label}"', 1)


def test_upload_style_from_path(test_geoserver: GeoServer) -> None:
    test_geoserver.upload_style(SLD_PATH, workspace=WORKSPACE)
    assert test_geoserver.style_exists("elevation", workspace=WORKSPACE)


def test_upload_style_from_content(test_geoserver: GeoServer) -> None:
    test_geoserver.upload_style(sld(), name="from-content", workspace=WORKSPACE)
    assert "ColorMap" in test_geoserver.download_style("from-content", workspace=WORKSPACE)


def test_upload_style_from_bytes_io(test_geoserver: GeoServer) -> None:
    test_geoserver.upload_style(io.BytesIO(sld().encode()), name="from-bytes-io", workspace=WORKSPACE)
    assert "ColorMap" in test_geoserver.download_style("from-bytes-io", workspace=WORKSPACE)


def test_upload_style_from_file_object(test_geoserver: GeoServer, tmp_path: Path) -> None:
    path = tmp_path / "from-file-object.sld"
    path.write_text(sld(), encoding="utf-8")
    with open(path, "rb") as f:
        test_geoserver.upload_style(f, workspace=WORKSPACE)

    # The name is inferred from the file name.
    assert "ColorMap" in test_geoserver.download_style("from-file-object", workspace=WORKSPACE)


def test_upload_style_keeps_non_ascii_text(test_geoserver: GeoServer) -> None:
    test_geoserver.upload_style(sld("Élévation 東京"), name="non-ascii", workspace=WORKSPACE)
    assert "Élévation 東京" in test_geoserver.download_style("non-ascii", workspace=WORKSPACE)


def test_upload_style_overwrite(test_geoserver: GeoServer) -> None:
    test_geoserver.upload_style(sld("before"), name="overwritten", workspace=WORKSPACE)

    with pytest.raises(GeoServerError):
        test_geoserver.upload_style(sld("after"), name="overwritten", workspace=WORKSPACE)

    test_geoserver.upload_style(sld("after"), name="overwritten", workspace=WORKSPACE, overwrite=True)
    assert 'label="after"' in test_geoserver.download_style("overwritten", workspace=WORKSPACE)


def test_upload_style_zip_in_workspace(test_geoserver: GeoServer, tmp_path: Path) -> None:
    archive = tmp_path / "zipped.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(SLD_PATH, arcname="zipped.sld")

    test_geoserver.upload_style(archive, workspace=WORKSPACE)

    # The zip is named after the file, not after the name inside the SLD ("raster", a default style).
    assert test_geoserver.style_exists("zipped", workspace=WORKSPACE)
    assert not test_geoserver.style_exists("zipped")


def test_upload_style_requires_a_name(test_geoserver: GeoServer) -> None:
    with pytest.raises(ValueError):
        test_geoserver.upload_style(sld(), workspace=WORKSPACE)
    with pytest.raises(ValueError):
        test_geoserver.upload_style(io.BytesIO(sld().encode()), workspace=WORKSPACE)
