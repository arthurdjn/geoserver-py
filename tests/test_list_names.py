import os
from pathlib import Path
from typing import Any, Generator

import pytest
from helpers import GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer

TEST_DATA_DIR = Path(__file__).parent / "data"
WORKSPACE = "test-list-names"
EMPTY_WORKSPACE = "test-list-names-empty"

pytestmark = pytest.mark.skipif(not GEOSERVER_RUNNING, reason=f"No GeoServer running at {GEOSERVER_URL!r}.")


@pytest.fixture(scope="module", autouse=True)
def catalog(test_geoserver: GeoServer) -> Generator[None, None, None]:
    """A workspace with two coverage stores, a data store, a style and a layer group, and an empty workspace."""
    for name in (WORKSPACE, EMPTY_WORKSPACE):
        if test_geoserver.workspace_exists(name):
            test_geoserver.delete_workspace(name, recurse=True)
        test_geoserver.create_workspace_from_name(name)

    raster = TEST_DATA_DIR / "rasters" / "raster.tif"
    test_geoserver.upload_coverage_store(raster, workspace=WORKSPACE, name="raster_a", format="geotiff")
    test_geoserver.upload_coverage_store(raster, workspace=WORKSPACE, name="raster_b", format="geotiff")
    test_geoserver.upload_data_store(TEST_DATA_DIR / "vectors" / "buildings.shp", workspace=WORKSPACE, name="vectors")
    test_geoserver.upload_style(TEST_DATA_DIR / "styles" / "elevation.sld", workspace=WORKSPACE)
    group = {"layerGroup": {"name": "group", "publishables": {"published": [{"@type": "layer", "name": "raster_a"}]}}}
    test_geoserver.create_layer_group(group, workspace=WORKSPACE)
    yield
    for name in (WORKSPACE, EMPTY_WORKSPACE):
        test_geoserver.delete_workspace(name, recurse=True)


def test_list_workspaces(test_geoserver: GeoServer) -> None:
    names = test_geoserver.list_workspaces()
    assert {WORKSPACE, EMPTY_WORKSPACE} <= set(names)


def test_list_stores(test_geoserver: GeoServer) -> None:
    assert test_geoserver.list_coverage_stores(workspace=WORKSPACE) == ["raster_a", "raster_b"]
    assert test_geoserver.list_data_stores(workspace=WORKSPACE) == ["vectors"]


def test_list_resources(test_geoserver: GeoServer) -> None:
    # An upload names the file, and so the coverage or feature type, after the store.
    assert test_geoserver.list_coverages(workspace=WORKSPACE) == ["raster_a", "raster_b"]
    assert test_geoserver.list_coverages(workspace=WORKSPACE, store="raster_b") == ["raster_b"]
    assert test_geoserver.list_feature_types(workspace=WORKSPACE, store="vectors") == ["vectors"]


def test_list_layers(test_geoserver: GeoServer) -> None:
    assert sorted(test_geoserver.list_layers(workspace=WORKSPACE)) == ["raster_a", "raster_b", "vectors"]
    assert f"{WORKSPACE}:raster_a" in test_geoserver.list_layers()


def test_list_layer_groups_and_styles(test_geoserver: GeoServer) -> None:
    assert test_geoserver.list_layer_groups(workspace=WORKSPACE) == ["group"]
    assert test_geoserver.list_styles(workspace=WORKSPACE) == ["elevation"]


@pytest.mark.parametrize(
    "call",
    [
        pytest.param(lambda gs: gs.list_data_stores(workspace=EMPTY_WORKSPACE), id="data_stores"),
        pytest.param(lambda gs: gs.list_coverage_stores(workspace=EMPTY_WORKSPACE), id="coverage_stores"),
        pytest.param(lambda gs: gs.list_coverages(workspace=EMPTY_WORKSPACE), id="coverages"),
        pytest.param(lambda gs: gs.list_feature_types(workspace=EMPTY_WORKSPACE), id="feature_types"),
        pytest.param(lambda gs: gs.list_layers(workspace=EMPTY_WORKSPACE), id="layers"),
        pytest.param(lambda gs: gs.list_layer_groups(workspace=EMPTY_WORKSPACE), id="layer_groups"),
        pytest.param(lambda gs: gs.list_styles(workspace=EMPTY_WORKSPACE), id="styles"),
    ],
)
def test_list_empty(test_geoserver: GeoServer, call: Any) -> None:
    # GeoServer answers "" for an empty collection.
    assert call(test_geoserver) == []


def test_list_available_feature_types_requires_store(test_geoserver: GeoServer) -> None:
    with pytest.raises(ValueError):
        test_geoserver.list_feature_types(workspace=WORKSPACE, available=True)


def test_list_available_feature_types(test_geoserver: GeoServer) -> None:
    psycopg2 = pytest.importorskip("psycopg2")
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST") or "localhost",
            port=os.getenv("POSTGRES_PORT") or "5432",
            dbname=os.getenv("POSTGRES_DB") or "db",
            user=os.getenv("POSTGRES_USER") or "admin",
            password=os.getenv("POSTGRES_PASSWORD") or "postgres",
        )
    except psycopg2.OperationalError:
        pytest.skip("No PostGIS running.")

    schema = "test_list_names"
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")
        cursor.execute(f"CREATE SCHEMA {schema}")
        cursor.execute(f"CREATE TABLE {schema}.published (id serial PRIMARY KEY, geom geometry(Point, 4326))")
        cursor.execute(f"CREATE TABLE {schema}.unpublished (id serial PRIMARY KEY, geom geometry(Point, 4326))")

    try:
        # GeoServer reaches the database by its docker compose service name.
        parameters = {
            "host": "postgis",
            "port": "5432",
            "database": os.getenv("POSTGRES_DB") or "db",
            "schema": schema,
            "user": os.getenv("POSTGRES_USER") or "admin",
            "passwd": os.getenv("POSTGRES_PASSWORD") or "postgres",
            "dbtype": "postgis",
        }
        entries = [{"@key": key, "$": value} for key, value in parameters.items()]
        body = {"dataStore": {"name": "database", "connectionParameters": {"entry": entries}}}
        test_geoserver.create_data_store(body, workspace=WORKSPACE)
        test_geoserver.create_feature_type(
            {"featureType": {"name": "published"}}, workspace=WORKSPACE, store="database"
        )

        available = test_geoserver.list_feature_types(workspace=WORKSPACE, store="database", available=True)
        assert available == ["unpublished"]
        assert test_geoserver.list_feature_types(workspace=WORKSPACE, store="database") == ["published"]
    finally:
        test_geoserver.delete_data_store("database", workspace=WORKSPACE, recurse=True)
        with connection.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA {schema} CASCADE")
        connection.close()
