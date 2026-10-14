import os
import subprocess
from typing import Generator

import pytest
from helpers import GEOSERVER_ADMIN_PASSWORD, GEOSERVER_ADMIN_USER, GEOSERVER_RUNNING, GEOSERVER_URL

from geoserver import GeoServer, GeoWebCache


def pytest_configure(config: pytest.Config) -> None:
    # The tests skip themselves when GeoServer is down, which silently turns a broken CI setup into a green run.
    if os.getenv("GEOSERVER_REQUIRED") and not GEOSERVER_RUNNING:
        raise pytest.UsageError(f"GEOSERVER_REQUIRED is set but no GeoServer is running at {GEOSERVER_URL!r}.")


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
    cmd = 'ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 user=admin dbname=db password=postgres" tests/data/vectors/landuse.shp -nlt PROMOTE_TO_MULTI -lco OVERWRITE=YES'
    subprocess.run(cmd, shell=True, check=False)
    yield None
