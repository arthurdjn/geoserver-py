import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoWebCache

# Blob stores


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_blob_stores(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_blob_stores()
    assert isinstance(data, list)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_blob_store(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_insert_blob_store(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_blob_store(test_geowebcache: GeoWebCache) -> None: ...


# Bounds


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_layer_bounds(test_geowebcache: GeoWebCache) -> None: ...


# Disk Quota


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_diskquota(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_diskquota()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_diskquota(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_filter_update(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_global_settings(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_global_settings()
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_update_global_settings(test_geowebcache: GeoWebCache) -> None:
    body = test_geowebcache.get_global_settings()
    body["global"]["backendTimeout"] = 100

    msg = test_geowebcache.update_global_settings(body=body)
    assert isinstance(msg, str)


# Gridsets


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_gridsets(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_gridsets()
    assert isinstance(data, list)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_gridset(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_insert_gridset(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_gridset(test_geowebcache: GeoWebCache) -> None: ...


# Layers


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_layers(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_layers()
    assert isinstance(data, list)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_layer(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_insert_layer(test_geowebcache: GeoWebCache) -> None: ...


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_layer(test_geowebcache: GeoWebCache) -> None: ...


# Mass Truncate


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_masstruncate(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_masstruncate()
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_masstruncate(test_geowebcache: GeoWebCache) -> None: ...


# Statistics


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_statistics(test_geowebcache: GeoWebCache) -> None: ...


# Reload


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reload(test_geowebcache: GeoWebCache) -> None:
    msg = test_geowebcache.reload(body="reload_configuration=1")
    assert isinstance(msg, str)


# Seed


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_seed(test_geowebcache: GeoWebCache) -> None:
    data = test_geowebcache.get_seed()
    assert isinstance(data, dict)
