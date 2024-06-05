from typing import Generator

import pytest

from geoserver import GeoServer

# Fixtures


@pytest.fixture(scope="module")
def workspace(test_geoserver: GeoServer) -> Generator[str, None, None]:
    workspace = "test-workspace"
    test_geoserver.create_workspace(body={"workspace": {"name": workspace}})
    yield workspace
    test_geoserver.delete_workspace(workspace=workspace, recurse=True)
