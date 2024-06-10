<div align="center" style="width: 100%; margin: auto">
  <a href="" rel="noopener"><img src="https://raw.githubusercontent.com/arthurdjn/geoserver-py/main/medias/geoserver-py.png" alt="Banner"></a>

[![python](https://img.shields.io/badge/python-3.8_%7C_3.9_%7C_3.10_%7C_3.11_%7C_3.12-red.svg?color=009ACF&labelColor=6DBA65&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/black-formatter-red.svg?color=009ACF&labelColor=6DBA65)](https://github.com/psf/black)
[![mypy](https://img.shields.io/badge/mypy-typing-red.svg?color=009ACF&labelColor=6DBA65)](https://mypy-lang.org)
[![ruff](https://img.shields.io/badge/ruff-linter-red.svg?color=009ACF&labelColor=6DBA65&logo=ruff&logoColor=white)](https://docs.astral.sh/ruff)
[![isort](https://img.shields.io/badge/isort-imports-red.svg?color=009ACF&labelColor=6DBA65)](https://pycqa.github.io/isort/)
[![poetry](https://img.shields.io/badge/poetry-dependencies-red.svg?color=009ACF&labelColor=6DBA65&logo=poetry&logoColor=white)](https://python-poetry.org)
[![pytest](https://img.shields.io/badge/pytest-testing-red.svg?color=009ACF&labelColor=6DBA65&logo=pytest&logoColor=white)](https://pytest.org)

</div>

---

<p align="center">
    Unofficial GeoServer python client. Manage workspaces, permissions, upload vectors, rasters and more. Check out the <a href="https://arthurdjn.github.io/geoserver-py">documentation</a> for more information! <br>
    <i>We are looking for contributors and feedbacks!</i>
</p>

<br>

## ❓ About

This python package provides a simple interface to communicate with GeoServer. It implements most of the GeoServer REST API endpoints, allowing users to interact with GeoServer programmatically.

### Why?

The purpose of this package is to implement the REST API endpoints with **full type hints** and **[documentation](https://arthurdjn.github.io/geoserver-py)**. This package does not aim to provide a high-level abstraction over the GeoServer REST API, thus it is expected that you have some knowledge of the GeoServer REST API.

### Features

This package supports both **JSON** and **XML** requests and response. It provides type hints for all the methods and classes, making it easier to work with the package.

> [!NOTE]
> This package only relies on `requests` as a dependency, which make it extremely lightweight and easy to install: no need to install GDAL!

> [!TIP]
> Check out the [documentation](https://arthurdjn.github.io/geoserver-py) for more information!

#### Get requests

```python
# As JSON
workspaces = geoserver.get_workspaces()  # default is "json"

# As XML
workspaces = geoserver.get_workspaces(format="xml")
```

#### Post requests

```python
# As JSON
geoserver.create_workspace(body={"workspace": {"name": "new_workspace"}})

# As XML
geoserver.create_workspace(body="<workspace><name>new_workspace</name></workspace>")
```

### Documentation

We provide several [examples](./notebooks) and a [documentation](https://docs.geoserver.org/main/en/user/rest/index.html) to help you get started,

<br>

## 🚀 Quick Start

This section will guide you on how to setup and use the package.

### Installation

```bash
pip install geoserver-py
```

### Usage

```python
from geoserver import GeoServer

# Connect to a GeoServer instance
geoserver = GeoServer(
    url="http://localhost:8080/geoserver",
    username="admin",
    password="geoserver"
)

# Get all workspaces
workspaces = geoserver.get_workspaces()

# Create a workspace
geoserver.create_workspace_from_name(name="my_workspace")
# or geoserver.create_workspace(body={"workspace": {"name": "my_workspace"}})

# Get all datastores
datastores = geoserver.get_data_stores(workspace="my_workspace")

# Upload a Shapefile
geoserver.upload_data_store(file="path/to/file.shp", workspace="my_workspace")

# Upload a GeoTIFF
geoserver.upload_coverage_store(file="path/to/file.tif", format="geotiff", workspace="my_workspace")

# Upload a style
geoserver.upload_style(file="path/to/file.sld", workspace="my_workspace")

# etc.
```

<br>

## 📚 Examples

We provide several examples in the [notebooks](./notebooks) folder. These examples are based on the [GeoServer REST API documentation](https://docs.geoserver.org/main/en/user/rest/index.html).

<br>

## 🤗 Contributing

We welcome any contributions, from bug reports to new features! If you want to contribute to the package, please read the [For Developers](#-for-developers) section.

If you simply find the package useful, please consider giving it a star ⭐️ on GitHub.

<br>

## 🧑‍💻 For Developers

This section if for advanced users who want to contribute to the package. It will guide you on how to setup the package for development.

### Local installation

1. First, clone the repository and install the dependencies:

    ```bash
    git clone https://github.com/arthurdjn/geoserver-py
    cd geoserver-py
    ```

2. Install the dependencies (we recommend using [`poetry`](https://python-poetry.org/) for this)

    ```bash
    poetry install
    ```

> [!NOTE]
> The usual workflow is to create a fork of the repository, clone it, and then install the dependencies.

### Testing

First, make sure you have a running GeoServer instance. You can run one using the provided `docker-compose` file:

```bash
docker-compose up -d
```

Then, you can run the tests using the following command:

```bash
make tests
```

### Linting, formatting and typing

You can run the linters, formatters and type checkers using the following command:

```bash
make lint     # Run all the below commands
make format   # Format the code using black
make type     # Type check the code using mypy
make isort    # Sort the imports using isort
make all      # Run all the above commands
```

### Before committing

Make sure to run the `pre-commit` hook before committing, which will check that the formatting, linting and typing are correct:

```bash
make pre-commit
```

> [!NOTE]
> Also make sure the tests are passing.

Once everything is correct, please **create a pull request** to the repository from your local fork.

### About versioning

We follow the [Semantic Versioning](https://semver.org/) guidelines for versioning the package. The version number is defined in the `pyproject.toml` file.

There are some utility commands to automate the versioning and publish associated tags:

```bash
make patch    # Bump the patch version
make minor    # Bump the minor version
make major    # Bump the major version
```

<br>

## 👉 Similar Projects

There are several alternatives to this package, some of them are:

- [`geoserver-rest`](https://github.com/gicait/geoserver-rest) is a Python library for management for geospatial data in GeoServer.
- [`geoserver-restconfig`](https://github.com/GeoNode/geoserver-restconfig) is a python library for manipulating a GeoServer instance via the GeoServer RESTConfig API.

While these packages are great and well-maintained, they do not provide full type hints and customizations over the GeoServer REST API. This library aims to provide a closer API to the GeoServer REST API, making it easier to work with the package.

_We would like to thank the authors of these packages for their contributions to the community, which have inspired us to create `geoserver-py`._
