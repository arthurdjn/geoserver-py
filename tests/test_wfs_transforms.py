import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
)

from geoserver import GeoServer

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
