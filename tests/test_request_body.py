from typing import Any, Dict

import pytest
import requests

from geoserver import GeoServer, GeoWebCache


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> Dict[str, Any]:
    """Captures the arguments of the HTTP request instead of sending it."""
    captured: Dict[str, Any] = {}

    def fake_request(session: requests.Session, method: str, url: str, **kwargs: Any) -> requests.Response:
        captured.update(kwargs, method=method, url=url)
        response = requests.Response()
        response.status_code = 201
        return response

    monkeypatch.setattr(requests.Session, "request", fake_request)
    return captured


def test_external_upload_sends_the_path(sent: Dict[str, Any]) -> None:
    geoserver = GeoServer("http://geoserver")
    geoserver.upload_coverage_store("/data/raster.tif", method="external", workspace="ws", format="geotiff")

    assert sent["url"] == "http://geoserver/rest/workspaces/ws/coveragestores/raster/external.geotiff"
    assert sent["data"] == "/data/raster.tif"


def test_url_upload_sends_the_url(sent: Dict[str, Any]) -> None:
    geoserver = GeoServer("http://geoserver")
    geoserver.upload_data_store("https://example.com/roads.zip", workspace="ws")

    assert sent["url"] == "http://geoserver/rest/workspaces/ws/datastores/roads/url.shp"
    assert sent["data"] == "https://example.com/roads.zip"


def test_geowebcache_reload_sends_the_body(sent: Dict[str, Any]) -> None:
    GeoWebCache("http://geoserver").reload("reload_configuration=1")

    assert sent["data"] == "reload_configuration=1"
