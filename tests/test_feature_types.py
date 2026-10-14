from typing import Optional

import pytest
from helpers import (
    GEOSERVER_RUNNING,
    GEOSERVER_URL,
    TEST_DATA_STORE,
)
from pytest import FixtureRequest

from geoserver import GeoServer

# Feature Types


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_get_feature_types(test_geoserver: GeoServer, test_workspace: str, test_data_store: str) -> None:
    data = test_geoserver.get_feature_types(workspace=test_workspace)
    assert isinstance(data, dict)

    data = test_geoserver.get_feature_types(workspace=test_workspace, store=test_data_store)
    assert isinstance(data, dict)


@pytest.mark.skip("Not implemented yet.")
@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_create_feature_type(test_geoserver: GeoServer) -> None: ...


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("store", [None, TEST_DATA_STORE])
def test_get_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    store: Optional[str],
    request: FixtureRequest,
) -> None:
    if store == TEST_DATA_STORE:
        store = request.getfixturevalue(store)

    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=store)
    assert isinstance(data, dict)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
@pytest.mark.parametrize("recalculate", [None, "", "nativebbox", "nativebbox,latlonbbox"])
def test_update_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
    recalculate: Optional[str],
) -> None:
    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert isinstance(data, dict)

    data["featureType"]["title"] = "Updated title"
    msg = test_geoserver.update_feature_type(
        test_feature_type,
        workspace=test_workspace,
        body=data,
        store=test_data_store,
        recalculate=recalculate,  # type: ignore[arg-type]
    )
    assert isinstance(msg, str)

    data = test_geoserver.get_feature_type(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert data["featureType"]["title"] == "Updated title"


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_reset_feature_type_caches(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
) -> None:
    msg = test_geoserver.reset_feature_type_caches(test_feature_type, workspace=test_workspace, store=test_data_store)
    assert isinstance(msg, str)


@pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")
def test_delete_feature_type(
    test_geoserver: GeoServer,
    test_workspace: str,
    test_feature_type: str,
    test_data_store: str,
) -> None:
    msg = test_geoserver.delete_feature_type(
        test_feature_type,
        workspace=test_workspace,
        store=test_data_store,
        recurse=True,
    )
    assert isinstance(msg, str)
