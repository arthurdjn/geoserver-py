import subprocess
from typing import Generator

import pytest
from helpers import GEOSERVER_ADMIN_PASSWORD, GEOSERVER_ADMIN_USER, GEOSERVER_URL

from geoserver import GeoServer, GeoWebCache


@pytest.fixture(scope="session", autouse=True)
def test_geoserver() -> Generator[GeoServer, None, None]:
    yield GeoServer(
        service_url=GEOSERVER_URL,
        username=GEOSERVER_ADMIN_USER,
        password=GEOSERVER_ADMIN_PASSWORD,
    )


@pytest.fixture(scope="session", autouse=True)
def test_geowebcache() -> Generator[GeoWebCache, None, None]:
    yield GeoWebCache(
        service_url=GEOSERVER_URL,
        username=GEOSERVER_ADMIN_USER,
        password=GEOSERVER_ADMIN_PASSWORD,
    )


@pytest.fixture(scope="session", autouse=True)
def test_postgis() -> Generator[None, None, None]:
    cmd = 'ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 user=admin dbname=db password=postgres" examples/vectors/jamoat-db.shp -nlt PROMOTE_TO_MULTI -lco OVERWRITE=YES'
    subprocess.run(cmd, shell=True, check=False)
    yield None
