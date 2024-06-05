# Welcome to geoserver-py

## About

`geoserver-py` is a Python client for the GeoServer REST API. It is designed to be simple and easy to use, while providing access to the full functionality of the GeoServer REST API.

## Installation

The `geoserver-py` package only requires the `requests` package as a dependency.
To install it, simply run:

```bash
pip install geoserver-py
```

## Quickstart

### Connecting to GeoServer

To get started with `geoserver-py`, you need to create a `GeoServer` object and provide the base URL of your GeoServer instance:

```python
from geoserver import GeoServer

geoserver = GeoServer(
    "http://localhost:8080/geoserver", 
    username="admin", 
    password="geoserver"
)
```

You can then use the `geoserver` object to interact with your GeoServer instance. For example, to list all workspaces:

```python
workspaces = geoserver.get_workspaces()
```

### Using XML or JSON requests

The API supports both XML and JSON requests. All methods are fully type-hinted, so you can use your IDE's autocompletion to see the available parameters and return types, based on the requested format.

For `POST` and `PUT` requests, you can specify the request body as either a dictionary (for JSON) or a string (for XML).

=== "Using JSON"

    ```python
    geoserver.create_workspace(
        body={"workspace": {"name": "new_workspace"}}
    )
    ```

=== "Using XML"

    ```python
    geoserver.create_workspace(
        body="<workspace><name>new_workspace</name></workspace>"
    )
    ```

Similarly, you can specify the returned format for `GET` requests using the `format` parameter:

=== "Using JSON"

    ```python
    workspaces = geoserver.get_workspaces(format="json")
    ```

=== "Using XML"

    ```python
    workspaces = geoserver.get_workspaces(format="xml")
    ```

### Error handling

The API will raise exceptions for any HTTP error responses. You can catch these exceptions and handle them as needed.

```python
from geoserver.exceptions import GeoServerError


try:
    # Already exists
    geoserver.create_workspace( 
        body={"workspace": {"name": "new_workspace"}}
    )
except GeoServerError as e:
    print(f"Status Code: {e.status_code}")
    print(f"Error: {e.message}")
```

## Contributing & Supporting

We welcome any contributions, from bug reports to new features! If you want to contribute to the package, please read the [For Developers](https://github.com/arthurdjn/geoserver-py#-for-developers) section.

If you simply find the package useful, please consider giving it a star ⭐️ on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/arthurdjn/geoserver-py/blob/main/LICENSE) file for details.
