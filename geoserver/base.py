from io import BufferedReader
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, List, Literal, Optional, Tuple, Type, TypedDict, TypeVar, Union

import requests
from requests.auth import AuthBase, HTTPBasicAuth
from typing_extensions import Unpack

from .exceptions import GeoServerError
from .utils import find_html_body, find_html_description_section, find_html_message_section, is_html

Timeout = Union[float, Tuple[float, float]]
BaseT = TypeVar("BaseT", bound="Base")


class RequestParams(TypedDict, total=False):
    data: Any
    json: Dict[str, Any]
    params: Dict[str, Any]
    headers: Dict[str, Any]
    auth: Optional[AuthBase]
    cookies: Dict[str, Any]
    allow_redirects: bool
    proxies: Any
    verify: bool
    cert: Optional[str]
    timeout: Optional[Timeout]


class Base:
    def __init__(
        self,
        service_url: str = "http://localhost:8080/geoserver",
        username: Optional[str] = None,
        password: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, Any]] = None,
        auth: Optional[AuthBase] = None,
        allow_redirects: bool = True,
        proxies: Any = None,
        verify: bool = True,
        cert: Optional[str] = None,
        timeout: Optional[Timeout] = None,
        session: Optional[requests.Session] = None,
    ):
        if auth is None and username is not None and password is not None:
            auth = HTTPBasicAuth(username, password)

        self.service_url = service_url.rstrip("/")
        self.auth = auth
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.allow_redirects = allow_redirects
        self.proxies = proxies or {}
        self.verify = verify
        self.cert = cert
        self.timeout = timeout
        self.session = session if session is not None else requests.Session()

    def close(self) -> None:
        """Closes the connections of the HTTP session. The client stays usable and reconnects when needed."""
        self.session.close()

    def __enter__(self: BaseT) -> BaseT:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()

    def _request(
        self,
        method: Literal["post", "get", "put", "delete", "head"],
        url: str,
        body: Optional[Union[str, Dict[str, Any]]] = None,
        file: Optional[Union[str, Path, BufferedReader]] = None,
        ignore: Optional[List[int]] = None,
        **kwargs: Unpack[RequestParams],
    ) -> requests.Response:
        if method.lower() not in ["get", "post", "put", "delete", "head"]:
            raise ValueError(f"Invalid method {method!r}")

        # Default parameters
        ignore = ignore or []
        params: RequestParams = dict(
            headers=self.headers.copy(),
            cookies=self.cookies.copy(),
            auth=self.auth,
            allow_redirects=self.allow_redirects,
            proxies=self.proxies.copy(),
            verify=self.verify,
            cert=self.cert,
        )

        # If a body is provided (POST or PUT request), add respective headers (XML or JSON support)
        if isinstance(body, dict):
            params["headers"].update({"Content-Type": "application/json"})
            params["json"] = body
        elif isinstance(body, str):
            params["headers"].update({"Content-Type": "text/xml"})
            params["data"] = body

        # Override default parameters with user-provided parameters
        params["params"] = kwargs.pop("params", {})
        params["headers"].update({**kwargs.pop("headers", {})})
        params["cookies"].update({**kwargs.pop("cookies", {})})
        params["auth"] = kwargs.pop("auth", self.auth)
        params["proxies"].update(kwargs.pop("proxies", {}))
        params["allow_redirects"] = kwargs.pop("allow_redirects", self.allow_redirects)
        params["verify"] = kwargs.pop("verify", self.verify)
        params["cert"] = kwargs.pop("cert", self.cert)
        params["timeout"] = kwargs.pop("timeout", self.timeout)

        if file is None or not isinstance(file, (str, Path)):
            response = self.session.request(method.lower(), url, **params)
        else:
            with open(file, "rb") as f:
                params["data"] = f
                response = self.session.request(method.lower(), url, **params)

        # Handle errors
        if not response.ok and response.status_code not in ignore:
            message = response.text
            if is_html(message):
                body = find_html_body(message)
                message = find_html_message_section(body).strip()
                if message:
                    message += ". " if not message.endswith(".") else " "
                message += find_html_description_section(body)
            raise GeoServerError(message=message, status_code=response.status_code)
        return response
