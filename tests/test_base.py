import socket
import threading
from typing import Any, Dict, Generator, List

import pytest
import requests

from geoserver import GeoServer, GeoWebCache


class RecordingSession(requests.Session):
    """A session that records the requests instead of sending them."""

    def __init__(self) -> None:
        super().__init__()
        self.calls: List[Dict[str, Any]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:  # type: ignore[override]
        self.calls.append(dict(kwargs, method=method, url=url))
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"workspaces": ""}'
        return response


@pytest.fixture
def silent_server() -> Generator[str, None, None]:
    """The URL of a server that accepts connections but never answers."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen()
    connections: List[socket.socket] = []

    def accept() -> None:
        while True:
            try:
                connection, _ = server.accept()
            except OSError:
                return
            connections.append(connection)

    threading.Thread(target=accept, daemon=True).start()
    yield f"http://127.0.0.1:{server.getsockname()[1]}/geoserver"
    server.close()
    for connection in connections:
        connection.close()


def test_requests_go_through_the_session() -> None:
    session = RecordingSession()
    geoserver = GeoServer("http://geoserver", session=session)

    geoserver.get_workspaces()
    geoserver.get_workspaces()

    assert geoserver.session is session
    assert [call["url"] for call in session.calls] == ["http://geoserver/rest/workspaces.json"] * 2


def test_default_session_is_reused() -> None:
    geoserver = GeoWebCache("http://geoserver")
    assert isinstance(geoserver.session, requests.Session)
    assert geoserver.session is geoserver.session


def test_timeout_is_sent_with_every_request() -> None:
    session = RecordingSession()
    GeoServer("http://geoserver", session=session, timeout=(3.05, 27)).get_workspaces()
    assert session.calls[0]["timeout"] == (3.05, 27)


def test_timeout_can_be_changed() -> None:
    session = RecordingSession()
    geoserver = GeoServer("http://geoserver", session=session, timeout=10)
    geoserver.timeout = 600
    geoserver.get_workspaces()
    assert session.calls[0]["timeout"] == 600


def test_no_timeout_by_default() -> None:
    session = RecordingSession()
    GeoServer("http://geoserver", session=session).get_workspaces()
    assert session.calls[0]["timeout"] is None


def test_timeout_raises(silent_server: str) -> None:
    geoserver = GeoServer(silent_server, timeout=0.2)
    with pytest.raises(requests.exceptions.ReadTimeout):
        geoserver.get_workspaces()


def test_context_manager_closes_the_session(monkeypatch: pytest.MonkeyPatch) -> None:
    closed: List[bool] = []
    with GeoServer("http://geoserver") as geoserver:
        assert isinstance(geoserver, GeoServer)
        monkeypatch.setattr(geoserver.session, "close", lambda: closed.append(True))
    assert closed == [True]
