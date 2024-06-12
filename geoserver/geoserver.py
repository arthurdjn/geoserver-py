import re
import zipfile
from io import BufferedReader
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union, overload

from .base import Base
from .consts import CREATED_MESSAGE, DELETED_MESSAGE, OK_MESSAGE, UPDATED_MESSAGE


class GeoServer(Base):
    """
    GeoServer Client for Python. Use this class to interact with a GeoServer instance.

    Note:
        This class implements most of the GeoServer REST API endpoints.
        You can follow the official GeoServer REST API documentation [here](https://docs.geoserver.org/stable/en/user/rest/).

    Args:
        service_url: The URL of the GeoServer instance.
        username: The username to authenticate with the GeoServer instance.
        password: The password to authenticate with the GeoServer instance.
        headers: The headers to be included in the requests.
        cookies: The cookies to be included in the requests.
        auth: The authentication to be included in the requests.
        allow_redirects: A boolean indicating whether or not the requests should follow redirects.
        proxies: The proxies to be included in the requests.
        verify: A boolean indicating whether or not the SSL certificates should be verified.
        cert: The certificate to be included in the requests.

    Example:
        ```python
        from geoserver import GeoServer

        geoserver = GeoServer(
            service_url="http://localhost:8080/geoserver",
            username="admin",
            password="geoserver"
        )
        ```
    """

    # Manifests

    @overload
    def get_manifest(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_manifest(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_manifest(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves the manifest of the GeoServer instance, in JSON format.

        Args:
            manifest: Optional. The manifest parameter is used to filter over resulting resource (manifest) names attribute using Java regular expressions. Defaults to None.
            key: Optional. Only return manifest entries with this key in their properties. It can be optionally combined with the value parameter. Defaults to None.
            value: Optional. Only return manifest entries that have this value for the provided key parameter. Defaults to None.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The manifest of the GeoServer instance.

        Example:
            To get the manifest of the GeoServer instance, use the following code:

            ```python
            geoserver.get_manifest()
            ```

        """
        url = f"{self.service_url}/rest/about/manifest.{format}"
        params = dict(manifest=manifest, key=key, value=value)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    @overload
    def get_version(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_version(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_version(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Shows only the details for the high-level components: GeoServer, GeoTools, and GeoWebCache

        Args:
            manifest: Optional. The manifest parameter is used to filter over resulting resource (manifest) names attribute using Java regular expressions. Defaults to None.
            key: Optional. Only return manifest entries with this key in their properties. It can be optionally combined with the value parameter. Defaults to None.
            value: Optional. Only return manifest entries that have this value for the provided key parameter. Defaults to None.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The version of the GeoServer instance.

        Example:
            To get the version of the GeoServer instance, use the following code:

            ```python
            geoserver.get_version()
            ```
        """
        url = f"{self.service_url}/rest/about/version.{format}"
        params = dict(manifest=manifest, key=key, value=value)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    @overload
    def get_status(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_status(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_status(
        self,
        *,
        manifest: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Shows the status details of all installed and configured modules. Status details always include human readable name, and module name. Optional details include version, availability, status message, and links to documentation.

        Args:
            manifest: Optional. The manifest parameter is used to filter over resulting resource (manifest) names attribute using Java regular expressions. Defaults to None.
            key: Optional. Only return manifest entries with this key in their properties. It can be optionally combined with the value parameter. Defaults to None.
            value: Optional. Only return manifest entries that have this value for the provided key parameter. Defaults to None.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The version of the GeoServer instance.

        Example:
            To get the status of the GeoServer instance, use the following code:

            ```python
            geoserver.get_status()
            ```
        """
        url = f"{self.service_url}/rest/about/status.{format}"
        params = dict(manifest=manifest, key=key, value=value)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    # System Status

    @overload
    def get_system_status(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_system_status(self, *, format: Literal["xml"]) -> str: ...

    @overload
    def get_system_status(self, *, format: Literal["html"]) -> str: ...

    def get_system_status(self, *, format: Literal["json", "xml", "html"] = "json") -> Union[str, Dict[str, Any]]:
        """Returns a list of system-level information. Major operating systems (Linux, Windows and MacOX) are supported out of the box.

        Returns:
            The system status of the GeoServer instance.

        Example:
            To get the system status of the GeoServer instance, use the following code:

            ```python
            geoserver.get_system_status()
            ```
        """
        url = f"{self.service_url}/rest/about/system-status.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # Data Stores

    @overload
    def get_data_stores(self, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_data_stores(self, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_data_stores(self, *, workspace: str, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """List all data stores in workspace ws.

        Args:
            workspace: The name of the workspace containing the data stores.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The list of all datastores in the workspace.

        Example:
            To get the list of all data stores in the workspace, use the following code:

            ```python
            geoserver.get_data_stores(workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def data_store_exists(self, name: str, *, workspace: str) -> bool:
        """Check if a data store exists in a workspace.

        Args:
            name: The name of the data store.
            workspace: The name of the workspace containing the data stores.

        Returns:
            True if the data store exists, False otherwise.

        Example:
            To check if a data store exists in a workspace, use the following code:

            ```python
            geoserver.data_store_exists("my_data_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}.xml"
        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_data_store(self, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Adds a new data store to the workspace.

        Args:
            body: The body of the request used to create the data store.
            workspace: The name of the workspace containing the data stores.

        Returns:
            The data store created.

        Example:
            To create a new data store in a workspace, use the following code:

            ```python
            body = \"\"\"
            <dataStore>
                <name>my_data_store</name>
                <connectionParameters>
                    <entry key="host">localhost</entry>
                    <entry key="port">5432</entry>
                    <entry key="database">my_database</entry>
                    <entry key="user">my_user</entry>
                    <entry key="passwd">my_password</entry>
                    <entry key="dbtype">postgis</entry>
                </connectionParameters>
            </dataStore>
            \"\"\"

            geoserver.create_data_store(body, workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    # TODO: Update docs
    def upload_data_store(
        self,
        file: Union[str, Path, BufferedReader],
        *,
        workspace: str,
        name: Optional[str] = None,
        filename: Optional[str] = None,
        format: str = "shp",
        configure: Literal["none", "all"] = "all",
        overwrite: bool = False,
    ) -> str:
        """Uploads a new or update an existing data store from a local file.

        Note:
            The `store` parameter is automatically inferred from the file, if not provided.
            In case the file is a buffer, the `store` parameter is required.

        Note:
            The file name of the resource can be overwritten by:
            - Providing the `filename` parameter.
            - Using the `name` parameter. In this case, if the `filename` is not provided,
                the file name will be the same as the store name.

        Args:
            file: The file to upload.
            workspace: The name of the workspace.
            name: Optional. The name of the data store.
            filename:  Optional. The filename parameter specifies the target file name for a file that needs to be harvested as part of a mosaic.
                This is important to avoid clashes and to make sure the right dimension values are available in the name for multidimensional mosaics to work.
                Only used if method="file".

        Returns:
            Success message.

        Example:
            To upload a new data store from a local file, use the following code:

            ```python
            geoserver.upload_data_store("my_shapefile.zip", workspace="my_workspace", name="my_data_store")
            ```

            Or, using a buffer:

            ```python
            with open("my_shapefile.zip", "rb") as f:
                geoserver.upload_data_store(f, workspace="my_workspace", name="my_data_store")
            ```
        """
        if isinstance(file, Path):
            file = file.as_posix()
        if isinstance(file, str):
            name = name or Path(file).stem
            filename = filename or f"{name}.{Path(file).suffix[1:]}"
        if name is None:
            raise ValueError("The `store` parameter is required.")

        headers = {}
        if zipfile.is_zipfile(file):
            headers["Content-Type"] = "application/zip"

        params = dict(filename=filename, configure=configure)
        if overwrite:
            params["update"] = "overwrite"

        if isinstance(file, str) and file.startswith(("file:", "http://", "https://")):
            headers["Content-Type"] = "text/plain"
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}/external.{format}"
            self._request(method="put", url=url, data=file, params=params, headers=headers)
            return CREATED_MESSAGE

        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}/file.{format}"
        self._request(method="put", url=url, file=file, params=params, headers=headers)
        return CREATED_MESSAGE

    @overload
    def get_data_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_data_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["xml"]
    ) -> str: ...

    def get_data_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Controls a particular data store in a given workspace.

        Args:
            name: The name of the data store.
            workspace: The name of the workspace containing the data stores.
            quiet_on_not_found: Optional. If true, the server will not report an error if the data store is not found.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The requested data store.

        Example:
            To get the data store, use the following code:

            ```python
            geoserver.get_data_store("my_data_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}.{format}"
        params = dict(quietOnNotFound=quiet_on_not_found)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def update_data_store(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Modify a data store from a workspace.

        Args:
            name: The name of the data store to modify.
            workspace: The name of the workspace containing the data stores.
            body: The body of the request used to modify the data store.

        Returns:
            Success message.

        Example:
            To update a data store, use the following code:

            ```python
            body = \"\"\"
            <dataStore>
                <name>my_new_data_store</name>
            </dataStore>
            \"\"\"

            geoserver.update_data_store("my_data_store", body, workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_data_store(self, name: str, *, workspace: str, recurse: bool = False) -> str:
        """Remove data store from workspace ws.

        Args:
            name: The name of the data store to remove.
            workspace: The name of the workspace containing the data stores.
            recurse: Optional. If true, all resources contained in the store are also removed. Defaults to `False`.

        Returns:
            Success message.

        Example:
            To delete a data store, use the following code:

            ```python
            geoserver.delete_data_store("my_data_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}"
        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    def reset_data_store_caches(self, name: str, *, workspace: str) -> str:
        """Resets caches for this data store.
        This operation is used to force GeoServer to drop caches associated to this data store,
        and reconnect to the vector source the next time it is needed by a request.
        This is useful as the store can keep state, such as a connection pool,
        and the structure of the feature types it's serving.

        Args:
            name: The name of the data store.
            workspace: The name of the workspace containing the data stores.

        Returns:
            Success message.

        Example:
            To reset the caches of a data store, use the following code:

            ```python
            geoserver.reset_data_store_caches("my_data_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{name}/reset"
        self._request(method="put", url=url)  # NOTE: Can also be a POST
        return OK_MESSAGE

    # TODO: Add MongoDB endpoints

    # Coverages

    @overload
    def get_coverages(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[str] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverages(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[str] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_coverages(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[str] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """List the coverages available for the provided workspace and data store.

        Args:
            workspace: The name of the workspace containing the data stores.
            store: Optional. The name of the data store.
            list: Optional. The list parameter is used to filter over resulting resource names attribute using Java regular expressions.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The list of all coverages in the workspace and data store.

        Example:
            To get the list of all coverages in a workspace, use the following code:

            ```python
            geoserver.get_coverages(workspace="my_workspace")
            ```

            To specify a coverage store, use the following code:

            ```python
            geoserver.get_coverages(workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coverages.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages.{format}"

        response = self._request(method="get", url=url, params=dict(list=list))
        return response.json() if format == "json" else response.text

    def create_coverage(self, body: Union[str, Dict[str, Any]], *, workspace: str, store: Optional[str] = None) -> str:
        """Creates a new coverage, the underlying data store must exist.

        Args:
            body: The body the coverage to be created.
            workspace: The name of the workspace.
            store: Optional. The name of the coverage store.

        Returns:
            The created coverage.

        Example:
            To create a new coverage, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.create_coverage(body, workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coverages"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_coverage(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverage(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_coverage(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual coverage.

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace.
            store: Optional. The name of the coverage datastore. Defaults to None.
            quiet_on_not_found: Optional. If true, the server will not report an error if the coverage is not found.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested coverage.

        Example:
            To get a coverage, use the following code:

            ```python
            geoserver.get_coverage("my_coverage", workspace="my_workspace")
            ```

            To specify a coverage store, use the following code:

            ```python
            geoserver.get_coverage("my_coverage", workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coverages/{name}.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}.{format}"

        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json() if format == "json" else response.text

    @overload
    def get_coverage_index(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverage_index(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_coverage_index(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual coverage index structure.

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace.
            store: Optional. The name of the coverage datastore. Defaults to None.
            quiet_on_not_found: Optional. If true, the server will not report an error if the coverage is not found.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested coverage.

        Example:
            To get a coverage index, use the following code:

            ```python
            geoserver.get_coverage_index("my_coverage", workspace="my_workspace")
            ```

            To specify a coverage store, use the following code:

            ```python
            geoserver.get_coverage_index("my_coverage", workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coverages/{name}/index.{format}"
        if store is not None:
            url = (
                f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}/index.{format}"
            )

        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json() if format == "json" else response.text

    def update_coverage(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str, store: str) -> str:
        """Update an individual coverage

        Args:
            name: The name of the coverage.
            body: The body of the request used to update the coverage.
            workspace: The name of the workspace.
            store: The name of the coverage datastore

        Returns:
            Success message.

        Example:
            To update a coverage, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.update_coverage("my_coverage", body, workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_coverage(self, name: str, *, workspace: str, store: str, recurse: bool = False) -> str:
        """Delete a coverage (optionally recursively deleting layers).

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace.
            store: The name of the coverage datastore
            recurse: Optional. If true all stores containing the resource are also removed.

        Returns:
            Success message.

        Example:
            To delete a coverage, use the following code:

            ```python
            geoserver.delete_coverage("my_coverage", workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}"
        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    def reset_coverage_caches(self, name: str, *, workspace: str, store: str) -> str:
        """Resets raster caches for this coverage.
        This operation is used to force GeoServer to drop caches associated to this coverage,
        and reconnect to the raster source the next time it is needed by a request.
        This is useful as the readers often cache some information about the bounds,
        coordinate system and image structure that might have changed in the meantime.
        Warning, the band structure is stored as part of the coverage configuration and won't be modified by this call,
        in case of need it should be modified issuing a PUT request against the coverage resource itself.

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace.
            store: The name of the coverage datastore

        Returns:
            Success message.

        Example:
            To reset the caches of a coverage, use the following code:

            ```python
            geoserver.reset_coverage_caches("my_coverage", workspace="my_workspace", store="my_coverage_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}/reset"
        self._request(method="put", url=url)  # NOTE: Can also be a POST
        return OK_MESSAGE

    # Coverage Stores

    @overload
    def get_coverage_stores(self, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_coverage_stores(self, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_coverage_stores(
        self, *, workspace: str, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all styles on the server.

        Args:
            workspace: The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The list of all coverage stores in the workspace.

        Example:
            To get the list of all coverage stores in a workspace, use the following code:

            ```python
            geoserver.get_coverage_stores(workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def coveragestore_exists(self, name: str, *, workspace: str) -> bool:
        """Check if a coverage store exists in a workspace.

        Args:
            name: The name of the coverage store.
            workspace: The name of the workspace containing the coverage stores.

        Returns:
            True if the coverage store exists, False otherwise.

        Example:
            To check if a coverage store exists in a workspace, use the following code:

            ```python
            geoserver.coveragestore_exists("my_coverage_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}.xml"
        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_coverage_store(self, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Adds a new coverage store.

        Warning:
            It is preferred to use the `upload_coverage_store` method to upload a new coverage store.

        Args:
            body: The body of the request used to create the coverage store.
            workspace: The name of the workspace.

        Returns:
            Success message.

        Example:
            To create a new coverage store, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.create_coverage_store(body, workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    # TODO: Update docs
    def upload_coverage_store(
        self,
        file: Union[str, Path, BufferedReader],
        *,
        workspace: str,
        name: Optional[str] = None,
        method: Literal["auto", "file", "external", "url", "remote"] = "auto",
        format: Literal["geotiff", "worldimage", "imagemosaic"],
        update_bbox: bool = False,
        configure: Literal["none", "all"] = "all",
        use_jai_imageread: bool = False,
        coverage_name: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> str:
        """Adds a new or update an existing coverage store from a local file.

        Tip:
            This method is the preferred way to upload a new coverage store.

        Note:
            The `store` parameter is automatically inferred from the file, if not provided.
            In case the file is a buffer, the `store` parameter is required.

        Note:
            The file name of the resource can be overwritten by:
            - Providing the `filename` parameter.
            - Using the `store` parameter. In this case, if the `filename` is not provided,
                the file name will be the same as the store name.

        Args:
            file: The file to upload.
            workspace: The name of the workspace.
            name: Optional. The name of the coverage store.
            filename:  Optional. The filename parameter specifies the target file name for a file that needs to be harvested as part of a mosaic.
                This is important to avoid clashes and to make sure the right dimension values are available in the name for multidimensional mosaics to work.
                Only used if method="file".
            format: The type of the file. Must be one of "geotiff", "worldimage", or "imagemosaic".
            update_bbox: When set to `True`, triggers re-calculation of the layer native bbox. Defaults to `False`.

        Returns:
            Success message.

        Example:
            To upload a new coverage store from a local file, use the following code:

            ```python
            geoserver.upload_coverage_store("my_coverage_store.zip", workspace="my_workspace", name="my_coverage_store", format="geotiff")
            ```

            Or, using a buffer:

            ```python
            with open("my_coverage_store.zip", "rb") as f:
                geoserver.upload_coverage_store(f, workspace="my_workspace", name="my_coverage_store", format="geotiff")
            ```
        """
        if isinstance(file, Path):
            file = file.as_posix()
        if isinstance(file, str):
            name = name or Path(file).stem
            filename = filename or f"{name}.{Path(file).suffix[1:]}"

        if name is None:
            raise ValueError("The `name` parameter is required")

        headers = {}
        if zipfile.is_zipfile(file):
            headers["Content-Type"] = "application/zip"

        params = dict(
            update=update_bbox,
            filename=filename,
            configure=configure,
            USE_JAI_IMAGEREAD=use_jai_imageread,
            coverage_name=coverage_name,
        )

        if method == "auto":
            if isinstance(file, str) and file.startswith(("file:")):
                method = "external"
            elif isinstance(file, str) and file.startswith(("http://", "https://")):
                method = "url"

        if isinstance(file, str) and method in ["external", "url", "remote"]:
            headers["Content-Type"] = "text/plain"
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}/{method}.{format}"
            self._request(method="put", url=url, data=file, params=params, headers=headers)
            return CREATED_MESSAGE

        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}/file.{format}"
        self._request(method="put", url=url, file=file, params=params, headers=headers)
        return CREATED_MESSAGE

    @overload
    def get_coverage_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverage_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["xml"]
    ) -> str: ...

    def get_coverage_store(
        self, name: str, *, workspace: str, quiet_on_not_found: bool = False, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual coverage store.

        Args:
            name: The name of the coverage store.
            workspace: The name of the workspace.
            quiet_on_not_found: Optional. If true, the server will not report an error if the coverage store is not found.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested coverage store.

        Example:
            To get a coverage store, use the following code:

            ```python
            geoserver.get_coverage_store("my_coverage_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}.{format}"
        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json()

    def update_coverage_store(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Modifies a single coverage store.

        Args:
            name: The name of the coverage store.
            body: The body of the request used to update the coverage store.
            workspace: The name of the workspace.

        Returns:
            Success message.

        Example:
            To update a coverage store, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.update_coverage_store("my_coverage_store", body, workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_coverage_store(
        self, name: str, *, workspace: str, purge: Literal["none", "metadata", "all"] = "all", recurse: bool = False
    ) -> str:
        """Deletes a coverage store.

        Args:
            name: The name of the coverage store.
            workspace: The name of the workspace.
            purge: Optional. The purge parameter specifies if and how the underlying raster data source is deleted.
                When set to "none" data and auxiliary files are preserved.
                When set to "metadata" delete only auxiliary files and metadata.
                It's recommended when data files (such as granules) should not be deleted from disk.
                Finally, when set to "all both data and auxiliary files are removed.
                Defaults to "none".
            recurse: Optional. The recurse controls recursive deletion.
                When set to true all resources contained in the store are also removed.
                The default to false.

        Returns:
            Success message.

        Example:
            To delete a coverage store, use the following code:

            ```python
            geoserver.delete_coverage_store("my_coverage_store", workspace="my_workspace")
            ```

            To remove all resources contained in the store, use the following code:

            ```python
            geoserver.delete_coverage_store("my_coverage_store", workspace="my_workspace", recurse=True)
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}"
        params = dict(purge=purge, recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    def reset_coverage_store_caches(self, name: str, *, workspace: str) -> str:
        """Resets raster caches for this coverage store.
        This operation is used to force GeoServer to drop caches associated to this coverage store,
        and reconnect to the raster source the next time it is needed by a request.
        This is useful as the readers often cache some information about the bounds,
        coordinate system and image structure that might have changed in the meantime.

        Args:
            name: The name of the coverage store.
            workspace: The name of the workspace.

        Returns:
            Success message.

        Example:
            To reset the caches of a coverage store, use the following code:

            ```python
            geoserver.reset_coverage_store_caches("my_coverage_store", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{name}/reset"
        self._request(method="put", url=url)
        return OK_MESSAGE

    # Feature Types

    @overload
    def get_feature_types(
        self, *, workspace: str, store: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_feature_types(self, *, workspace: str, store: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_feature_types(
        self, *, workspace: str, store: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """List all feature types in the workspace.

        Args:
            workspace: The name of the workspace.
            store: The name of the data store.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The list of all feature types in the workspace.

        Example:
            To get the list of all feature types in a workspace, use the following code:

            ```python
            geoserver.get_feature_types(workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_feature_type(
        self, body: Union[str, Dict[str, Any]], *, workspace: str, store: Optional[str] = None
    ) -> str:
        """Create a new feature type.

        Note:
            When creating a new feature type via POST, if no underlying dataset
            with the specified name exists an attempt will be made to create it.
            This will work only in cases where the underlying data format supports the creation of new types (such as a database).
            When creating a feature type in this manner the client should include all attribute information
            in the feature type representation.

        Args:
            body: The body of the request used to create the feature type.
            workspace: The name of the workspace.
            store: Optional. The name of the data store.

        Returns:
            Success message.

        Example:
            To create a new feature type, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.create_feature_type(body, workspace="my_workspace", store="my_data_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_feature_type(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_feature_type(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_feature_type(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual feature type.

        Args:
            name: The name of the feature type.
            workspace: The name of the workspace.
            store: Optional. The name of the data store.
            quiet_on_not_found: Optional. If true, the server will not report an error if the feature type is not found.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested feature type.

        Example:
            To get a feature type, use the following code:

            ```python
            geoserver.get_feature_type("my_feature_type", workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes/{name}.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes/{name}.{format}"

        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json() if format == "json" else response.text

    def update_feature_type(
        self,
        name: str,
        body: Union[str, Dict[str, Any]],
        *,
        workspace: str,
        store: Optional[str] = None,
        recalculate: Literal["", "nativebbox", "nativebbox,latlonbbox"] = "",
    ) -> str:
        """Update an individual feature type.

        Args:
            name: The name of the feature type.
            body: The body of the request used to modify the feature type.
            workspace: The name of the workspace.
            store: Optional. The name of the data store.
            recalculate: Optional. Specifies whether to recalculate properties for a feature type.
                Some properties of feature types are automatically recalculated when necessary.
                In particular, the native bounding box is recalculated when the projection or projection policy are changed,
                and the lat/lon bounding box is recalculated when the native bounding box is recalculated,
                or when a new native bounding box is explicitly provided in the request.
                (The native and lat/lon bounding boxes are not automatically recalculated when they are explicitly included in the request.)
                In addition, the client may explicitly request a fixed set of fields to calculate, by including a comma-separated list of their names in the recalculate parameter.
                The empty parameter 'recalculate=' is useful avoid slow recalculation when operating against large datasets as 'recalculate=' avoids calculating any fields,
                regardless of any changes to projection, projection policy, etc. The nativebbox parameter 'recalculate=nativebbox'
                is used recalculates the native bounding box, while avoiding recalculating the lat/lon bounding box. Recalculate parameters
                can be used in together - 'recalculate=nativebbox,latlonbbox' can be used after a bulk import to recalculate both
                the native bounding box and the lat/lon bounding box. Finally, 'recalculate=attributes' can be used to reset the attributes
                and reload them from the original vector source. Pay attention to its usage, if attributes were explicitly configured to
                perform attribute selection, renaming, and other transformations, such configuration will be lost, resetting the
                feature type to the list of attributes found in the vector data source.

        Returns:
            Success message.

        Example:
            To update a feature type, use the following code:

            ```python
            # Check the GeoServer official documentation for the body structure
            body = "..."

            geoserver.update_feature_type("my_feature_type", body, workspace="my_workspace")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes/{name}"

        params = dict(recalculate=recalculate)
        self._request(method="put", url=url, body=body, params=params)
        return UPDATED_MESSAGE

    def delete_feature_type(
        self, name: str, *, workspace: str, store: Optional[str] = None, recurse: bool = False
    ) -> str:
        """Delete an individual feature type.

        Args:
            name: The name of the feature type.
            workspace: The name of the workspace.
            store: Optional. The name of the data store.
            recurse: Optional. If true, all resources contained in the store are also removed.

        Returns:
            Success message.

        Example:
            To delete a feature type, use the following code:

            ```python
            geoserver.delete_feature_type("my_feature_type", workspace="my_workspace")
            ```

            To also remove all associated resources, use the following code:

            ```python
            geoserver.delete_feature_type("my_feature_type", workspace="my_workspace", recurse=True)
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes/{name}"

        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    def reset_feature_type_caches(self, name: str, *, workspace: str, store: Optional[str] = None) -> str:
        """Resets caches for this feature type.
        This operation is used to force GeoServer to drop caches associated to this feature type,
        and reconnect to the vector source the next time it is needed by a request.
        This is useful as the store can keep state, such as a connection pool,
        and the structure of the feature types it's serving.

        Args:
            name: The name of the feature type.
            workspace: The name of the workspace.
            store: Optional. The name of the data store.

        Returns:
            Success message.

        Example:
            To reset the caches of a feature type, use the following code:

            ```python
            geoserver.reset_feature_type_caches("my_feature_type", workspace="my_workspace")
            ```

            To specify a data store, use the following code:

            ```python
            geoserver.reset_feature_type_caches("my_feature_type", workspace="my_workspace", store="my_data_store")
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/featuretypes/{name}/reset"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/featuretypes/{name}/reset"

        self._request(method="put", url=url)
        return OK_MESSAGE

    # Fonts
    # NOTE: Fonts cannot be added, updated, or removed via the REST API.

    @overload
    def get_fonts(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_fonts(self, *, format: Literal["xml"]) -> str: ...

    def get_fonts(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """List all fonts available to GeoServer.

        Args:
            format: The format of the response. It can be either "json" or "xml".

        Returns:
            The list of all fonts available to GeoServer.

        Example:
            To get the list of all fonts available to GeoServer, use the following code:

            ```python
            geoserver.get_fonts()
            ```
        """
        url = f"{self.service_url}/rest/fonts.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # Layer Groups

    @overload
    def get_layer_groups(
        self, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_layer_groups(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_layer_groups(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """List all layer groups in the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The list of all layer groups in the workspace.

        Example:
            To get the list of all layer groups, use the following code:

            ```python
            geoserver.get_layer_groups()
            ```
        """
        url = f"{self.service_url}/rest/layergroups.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def layer_group_exists(self, name: str, *, workspace: Optional[str] = None) -> bool:
        """Check if a layer group exists.

        Args:
            name: The name of the layer group.
            workspace: Optional. The name of the workspace.

        Returns:
            True if the layer group exists, False otherwise.
        """
        url = f"{self.service_url}/rest/layergroups/{name}.xml"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups/{name}.xml"

        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_layer_group(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Create a new layer group.

        Args:
            body: The body of the request used to create the layer group.
            workspace: Optional. The name of the workspace.

        Returns:
            The created layer group.
        """
        url = f"{self.service_url}/rest/layergroups"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_layer_group(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_layer_group(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_layer_group(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual layer group.

        Args:
            name: The name of the layer group.
            workspace: Optional. The name of the workspace.
            quiet_on_not_found: Optional. If true, the server will not report an error if the layer group is not found.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The requested layer group.
        """
        url = f"{self.service_url}/rest/layergroups/{name}.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups/{name}.{format}"

        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json() if format == "json" else response.text

    def update_layer_group(
        self, name: str, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None
    ) -> str:
        """Update an individual layer group.

        Args:
            name: The name of the layer group.
            body: The body of the request used to modify the layer group.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/layergroups/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups/{name}"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_layer_group(self, name: str, *, workspace: Optional[str] = None) -> str:
        """Delete an individual layer group.

        Args:
            name: The name of the layer group.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/layergroups/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layergroups/{name}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Layers

    @overload
    def get_layers(self, *, workspace: Optional[str] = None, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_layers(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_layers(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """List all layers in the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The list of all layers in the workspace.
        """
        url = f"{self.service_url}/rest/layers.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_layer(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Creates a new layer.

        Args:
            body: The body of the request used to create the layer.
            workspace: Optional. The name of the workspace.

        Returns:
            The created layer.
        """
        url = f"{self.service_url}/rest/layers"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_layer(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_layer(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_layer(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Get an individual layer.

        Args:
            name: The name of the layer.
            workspace: Optional. The name of the workspace.
            quiet_on_not_found: Optional. If true, the server will not report an error if the layer is not found.
            format: Optional. The format of the response. It can be either "json" or "xml".

        Returns:
            The requested layer.
        """
        url = f"{self.service_url}/rest/layers/{name}.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}.{format}"

        response = self._request(method="get", url=url, params=dict(quietOnNotFound=quiet_on_not_found))
        return response.json() if format == "json" else response.text

    def update_layer(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Update an individual layer.

        Args:
            name: The name of the layer.
            body: The body of the request used to modify the layer.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/layers/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_layer(self, name: str, *, workspace: Optional[str] = None) -> str:
        """Delete an individual layer.

        Args:
            name: The name of the layer.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/layers/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Logging

    @overload
    def get_logging(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_logging(self, *, format: Literal["xml"]) -> str: ...

    def get_logging(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays a list of all logging settings on the server.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The logging settings.
        """
        url = f"{self.service_url}/rest/logging.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_logging(self, body: Union[str, Dict[str, Any]]) -> str:
        """Modify the logging settings on the server.

        Args:
            body: The body of the request used to modify the logging settings.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/logging"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    # Monitoring

    @overload
    def get_monitored_requests(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_monitored_requests(self, *, format: Literal["xml"]) -> str: ...

    def get_monitored_requests(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Returns a list of all requests known to the monitoring system.
        If no list of fields is specified, the full list will be returned,
        with the exception of Class, Body and Error fields.
        The HTML format return a summary of the requests,
        and links to the single request to gather details.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The monitoring requests.
        """
        url = f"{self.service_url}/rest/monitor/requests.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def delete_monitored_requests(self) -> str:
        """Removes a request from the monitoring system.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/monitor/requests"
        self._request(method="delete", url=url)
        return OK_MESSAGE

    @overload
    def get_monitored_request(self, id: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_monitored_request(self, id: str, *, format: Literal["xml"]) -> str: ...

    def get_monitored_request(self, id: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Returns the details of a single request.

        Args:
            id: The id of the request to retrieve.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The monitoring request.
        """
        url = f"{self.service_url}/rest/monitor/requests/{id}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # Namespaces

    @overload
    def get_namespaces(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_namespaces(self, *, format: Literal["xml"]) -> str: ...

    def get_namespaces(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """List all namespaces on the server.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The list of all namespaces on the server.
        """
        url = f"{self.service_url}/rest/namespaces.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_namespace(self, body: Union[str, Dict[str, Any]]) -> str:
        """Create a new namespace.

        Args:
            body: The body of the request used to create the namespace.

        Returns:
            The created namespace.
        """
        url = f"{self.service_url}/rest/namespaces"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_namespace(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_namespace(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_namespace(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Get an individual namespace.

        Args:
            name: The name of the namespace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested namespace.
        """
        url = f"{self.service_url}/rest/namespaces/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_namespace(self, name: str, body: Union[str, Dict[str, Any]]) -> str:
        """Update an individual namespace.

        Args:
            name: The name of the namespace.
            body: The body of the request used to modify the namespace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/namespaces/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_namespace(self, name: str) -> str:
        """Delete an individual namespace.

        Args:
            name: The name of the namespace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/namespaces/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Services Settings

    @overload
    def get_wms_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_wms_settings(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_wms_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Get the WMS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMS settings for the workspace.
        """
        url = f"{self.service_url}/rest/services/wms/settings.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wms/workspaces/{workspace}/settings.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wms_settings(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Update the WMS settings for the workspace.

        Args:
            body: The body of the request used to modify the WMS settings.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wms/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wms/workspaces/{workspace}/settings"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wms_settings(self, *, workspace: Optional[str] = None) -> str:
        """Delete the WMS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wms/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wms/workspaces/{workspace}/settings"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_wfs_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_wfs_settings(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_wfs_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Get the WFS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WFS settings for the workspace.
        """
        url = f"{self.service_url}/rest/services/wfs/settings.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wfs/workspaces/{workspace}/settings.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wfs_settings(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Update the WFS settings for the workspace.

        Args:
            body: The body of the request used to modify the WFS settings.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wfs/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wfs/workspaces/{workspace}/settings"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wfs_settings(self, *, workspace: Optional[str] = None) -> str:
        """Delete the WFS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wfs/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wfs/workspaces/{workspace}/settings"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_wcs_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_wcs_settings(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_wcs_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Get the WCS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WCS settings for the workspace.
        """
        url = f"{self.service_url}/rest/services/wcs/settings.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wcs/workspaces/{workspace}/settings.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wcs_settings(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Update the WCS settings for the workspace.

        Args:
            body: The body of the request used to modify the WCS settings.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wcs/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wcs/workspaces/{workspace}/settings"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wcs_settings(self, *, workspace: Optional[str] = None) -> str:
        """Delete the WCS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wcs/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wcs/workspaces/{workspace}/settings"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_wmts_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_wmts_settings(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_wmts_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Get the WMTS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMTS settings for the workspace.
        """
        url = f"{self.service_url}/rest/services/wmts/settings.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wmts/workspaces/{workspace}/settings.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wmts_settings(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Update the WMTS settings for the workspace.

        Args:
            body: The body of the request used to modify the WMTS settings.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wmts/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wmts/workspaces/{workspace}/settings"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wmts_settings(self, *, workspace: Optional[str] = None) -> str:
        """Delete the WMTS settings for the workspace.

        Args:
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/wmts/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/services/wmts/workspaces/{workspace}/settings"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_oseo_settings(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_oseo_settings(self, *, format: Literal["xml"]) -> str: ...

    def get_oseo_settings(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves Open Search for Earth Observation Service settings globally for the server.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The OSEO settings for the workspace.
        """
        url = f"{self.service_url}/rest/services/oseo/settings.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_oseo_settings(self, body: Union[str, Dict[str, Any]]) -> str:
        """Update the Open Search for Earth Observation Service settings globally for the server.

        Args:
            body: The body of the request used to modify the OSEO settings.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/services/oseo/settings"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    # Reload

    def reset(self) -> str:
        """Resets all store, raster, and schema caches.
        This operation is used to force GeoServer to drop all caches and store connections and reconnect
        to each of them the next time they are needed by a request.
        This is useful in case the stores themselves cache some information about the data structures
        they manage that may have changed in the meantime.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/reset"
        self._request(method="put", url=url)
        return OK_MESSAGE

    def reload(self) -> str:
        """Reloads the GeoServer catalog and configuration from disk.
        This operation is used in cases where an external tool has modified the on-disk configuration.
        This operation will also force GeoServer to drop any internal caches and reconnect to all data stores.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/reload"
        self._request(method="put", url=url)
        return OK_MESSAGE

    # Resource

    @overload
    def get_resource(
        self, path: str, *, operation: Literal["default", "metadata"] = "default", format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_resource(
        self, path: str, *, operation: Literal["default", "metadata"] = "default", format: Literal["xml"]
    ) -> str: ...

    def get_resource(
        self,
        path: str,
        *,
        operation: Literal["default", "metadata"] = "default",
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Download a resource, list contents of directory, or show formatted resource metadata.
        Response content depends upon parameters.
        With operation=default, if the request is made against a non-directory resource, the content of the resource is returned.

        Args:
            path: The path to the resource.
            operation: Optional. The type of resource to get. It can be either "default" or "metadata". Defaults to "default".
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The requested resource.

        Example:
            ```python
            geoserver.get_resource(resource="styles/default_point.sld", operation="default")
            ```
        """
        url = f"{self.service_url}/rest/resources/{path}.{format}"
        params = dict(operation=operation, format="json")
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def update_resource(self, path: str, body: Union[str, Dict[str, Any]]) -> str:
        """Upload/move/copy a resource, create directories on the fly (overwrite if exists). For move/copy operations, place source path in body. Copying is not supported for directories.

        Args:
            path: The path to the resource.
            body: The content of the resource to upload. In the case of a move or copy operation,
                this is instead the path to the source resource to move/copy from.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/resources/{path}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_resource(self, path: str) -> str:
        """Delete a resource (recursively if directory)

        Args:
            path: The full path to the resource. Required, but may be empty; a request to /resource references the top level resource directory.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/resources/{path}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    def resource_exists(self, path: str) -> bool:
        """Check if a resource exists.

        Args:
            path: The full path to the resource.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/resources/{path}"
        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    # Security

    @overload
    def get_master_password(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_master_password(self, *, format: Literal["xml"]) -> str: ...

    def get_master_password(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays the keystore password. HTTPS is strongly suggested, otherwise password will be sent in plain text.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The master password.
        """
        url = f"{self.service_url}/rest/security/masterpw.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_master_password(self, body: Union[str, Dict[str, Any]]) -> str:
        """Changes keystore password. Must supply current keystore password. HTTPS is strongly suggested, otherwise password will be sent in plain text.

        Args:
            body: The body of the request used to set the master password.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/masterpw"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def update_password(self, body: Union[str, Dict[str, Any]]) -> str:
        """Updates the password for the account used to issue the request.

        Args:
            body: The body of the request used to set the password.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/self/password"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    @overload
    def get_catalog_mode(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_catalog_mode(self, *, format: Literal["xml"]) -> str: ...

    def get_catalog_mode(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Gets the catalog mode, which specifies how GeoServer will advertise secured layers
        and behave when a secured layer is accessed without the necessary privileges.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The catalog mode.
        """
        url = f"{self.service_url}/rest/security/acl/catalog.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_catalog_mode(self, body: Union[str, Dict[str, Any]]) -> str:
        """Changes catalog mode. The mode must be one of HIDE, MIXED, or CHALLENGE.

        Args:
            body: The catalog mode information to upload.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/catalog"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    @overload
    def get_security_layers(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_security_layers(self, *, format: Literal["xml"]) -> str: ...

    def get_security_layers(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays the current layer-based security rules.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The security layers.
        """
        url = f"{self.service_url}/rest/security/acl/layers.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def security_layer_exists(self, rule: str) -> bool:
        """Check if a security layer exists.

        Args:
            rule: The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/layers/{rule}"
        response = self._request(method="head", url=url, ignore=[404, 405])
        return response.status_code == 200

    def create_security_layers(self, body: Union[str, Dict[str, Any]]) -> str:
        """Adds one or more new layer-based rules to the list of security rules.

        Args:
            body: The body of the request used to create the security layer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/layers"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    def update_security_layers(self, body: Union[str, Dict[str, Any]]) -> str:
        """Updates one or more layer-based security rules.

        Args:
            body: The body of the request used to modify the security layer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/layers"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_security_layer(self, rule: Optional[str] = None) -> str:
        """Removes one or more layer-based security rules from the list of security rules.
        The `rule` must specified in the last part of the URL and of the form <workspace>.<layer>.[r|w|a]

        Args:
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/layers"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/layers/{rule}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_security_services(
        self, *, rule: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_security_services(self, *, rule: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_security_services(
        self, *, rule: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays the current service-based security rules.

        Args:
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The security services.
        """
        url = f"{self.service_url}/rest/security/acl/services.{format}"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/services/{rule}.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_security_services(self, body: Union[str, Dict[str, Any]], *, rule: Optional[str] = None) -> str:
        """Adds one or more new service-based rules to the list of security rules.

        Args:
            body: The body of the request used to create the security services.
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/services"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/services/{rule}"

        self._request(method="post", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_security_services(self, *, rule: Optional[str] = None) -> str:
        """Removes one or more service-based security rules from the list of security rules.

        Args:
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/services"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/services/{rule}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_security_access(
        self, *, rule: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_security_access(self, *, rule: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_security_access(
        self, *, rule: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays the current REST access rules.

        Args:
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The security REST.
        """
        url = f"{self.service_url}/rest/security/acl/rest.{format}"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/{rule}.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_security_access(self, body: Union[str, Dict[str, Any]], *, rule: Optional[str] = None) -> str:
        """Adds one or more new REST access rules.

        Args:
            body: The body of the request used to create the security access.
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/rest"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/{rule}"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    def update_security_access(self, body: Union[str, Dict[str, Any]], *, rule: Optional[str] = None) -> str:
        """Updates one or more REST access rules.

        Args:
            body: The body of the request used to modify the security access.
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/rest"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/{rule}"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_security_access(self, body: Union[str, Dict[str, Any]], *, rule: Optional[str] = None) -> str:
        """Removes one or more REST access rules.

        Args:
            body: The body of the request used to delete the security access.
            rule: Optional. The specified rule, as the last part in the URI, e.g. /security/acl/layers/*.*.r

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/acl/rest"
        if rule is not None:
            url = f"{self.service_url}/rest/security/acl/{rule}"

        self._request(method="delete", url=url, body=body)
        return DELETED_MESSAGE

    # Settings

    @overload
    def get_settings(self, *, workspace: Optional[str] = None, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_settings(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_settings(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all global or workspace settings on the server.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The settings for the workspace.
        """
        url = f"{self.service_url}/rest/settings.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/settings.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_settings(self, body: Union[str, Dict[str, Any]], *, workspace: Optional[str] = None) -> str:
        """Updates global or workspace settings on the server.

        Args:
            body: The body of the request used to modify the settings.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/settings"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/settings"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_settings(self, *, workspace: str) -> str:
        """Deletes workspace settings on the server.

        Args:
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/settings"
        response = self._request(method="delete", url=url)
        return response.text

    def get_contact_settings(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays a list of all global contact settings on the server.
        This is a subset of what is available at the /settings endpoint.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The contact settings.
        """
        url = f"{self.service_url}/rest/settings/contact.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_contact_settings(self) -> str:
        """Updates global contact settings on the server.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/settings/contact"
        self._request(method="put", url=url)
        return UPDATED_MESSAGE

    # Structured Coverages

    @overload
    def get_coverage_granules(
        self, name: str, *, workspace: str, store: str, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverage_granules(self, name: str, *, workspace: str, store: str, format: Literal["xml"]) -> str: ...

    def get_coverage_granules(
        self, name: str, *, workspace: str, store: str, limit: int = -1, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all the attributes associated to a particular coverage's granules

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace containing the coverage stores.
            store: The name of the store.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The granules in the structured coverage store.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}/index/granules.{format}"
        params = dict(limit=limit) if limit >= 0 else {}
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def delete_coverage_granules(
        self,
        name: str,
        *,
        workspace: str,
        store: str,
        filter: str = "",
        purge: Literal["none", "metadata", "all"] = "none",
        update_bbox: bool = False,
    ) -> str:
        """Allows removing one or more granules from the index.

        Args:
            name: The name of the coverage.
            workspace: The name of the workspace containing the coverage stores.
            store: The name of the store.
            filter: Optional. A CQL filter to reduce the returned granules.
            purge: Optional. The purge parameter specifies if and how the underlying raster data source is deleted.
                Allowable values for this parameter are `none`, `metadata` and `all`. When set to `none` data and auxiliary files are preserved,
                only the registration in the mosaic is removed When set to `metadata` delete only auxiliary files and metadata
                (e.g. NetCDF sidecar indexes). It's recommended when data files (such as granules) should not be deleted from disk.
                Finally, when set to `all` both data and auxiliary files are removed.
            update_bbox: Optional. When set to True, triggers re-calculation of the layer native bbox. Defaults to False.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{name}/index/granules"
        params = dict(filter=filter, purge=purge, updateBBox=update_bbox)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    @overload
    def get_coverages_granule(
        self, name: str, *, workspace: str, store: str, coverage: str, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_coverages_granule(
        self, name: str, *, workspace: str, store: str, coverage: str, format: Literal["xml"]
    ) -> str: ...

    def get_coverages_granule(
        self, name: str, *, workspace: str, store: str, coverage: str, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all the attributes associated to a particular coverage's granule

        Args:
            name: The ID of the granule.
            workspace: The name of the workspace containing the coverage stores.
            store: The name of the store.
            coverage: The name of the coverage.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The granule in the structured coverage store.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{coverage}/granules/index/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def delete_coverage_granule(
        self, name: str, *, workspace: str, store: str, coverage: str, purge: bool = False, update_bbox: bool = False
    ) -> str:
        """Allows removing the specified granule.

        Args:
            name: The ID of the granule.
            workspace: The name of the workspace containing the coverage stores.
            store: The name of the store.
            coverage: The name of the coverage.
            purge: Optional. The purge parameter specifies if and how the underlying raster data source is deleted.
                Allowable values for this parameter are `none`, `metadata` and `all`. When set to `none` data and auxiliary files are preserved,
                only the registration in the mosaic is removed When set to `metadata` delete only auxiliary files and metadata
                (e.g. NetCDF sidecar indexes). It's recommended when data files (such as granules) should not be deleted from disk.
                Finally, when set to `all` both data and auxiliary files are removed.
            update_bbox: Optional. When set to True, triggers re-calculation of the layer native bbox. Defaults to False.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{store}/coverages/{coverage}/granules/index/{name}"
        params = dict(purge=purge, updateBBox=update_bbox)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    # Styles

    @overload
    def get_styles(self, *, workspace: Optional[str] = None, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_styles(self, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_styles(
        self, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all styles on the server.

        Args:
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The styles.
        """
        url = f"{self.service_url}/rest/styles.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def style_exists(self, name: str, *, workspace: Optional[str] = None) -> bool:
        """Check if a style exists.

        Args:
            name: The name of the style.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/styles/{name}.xml"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles/{name}.xml"

        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    @overload
    def get_style(
        self, name: str, *, workspace: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_style(self, name: str, *, workspace: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_style(
        self, name: str, *, workspace: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves a single style.

        Args:
            name: The name of the style.
            workspace: Optional. The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/styles/{name}.{format}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles/{name}.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_style(self, body: str, *, workspace: Optional[str] = None) -> str:
        """Creates a new style.

        Warning:
            This method only supports body in XML format.

        Args:
            body: The body of the request used to create the style.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.

        Example:
            ```python
            geoserver.create_style(body="<sld>...</sld>")
            ```
        """
        url = f"{self.service_url}/rest/styles"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def upload_style(
        self,
        file: Union[str, Path, BufferedReader],
        *,
        name: str,
        workspace: Optional[str] = None,
        overwrite: Literal[True],
    ) -> str: ...

    @overload
    def upload_style(
        self,
        file: Union[str, Path, BufferedReader],
        *,
        name: Optional[str] = None,
        workspace: Optional[str] = None,
        overwrite: Literal[False] = False,
    ) -> str: ...

    def upload_style(
        self,
        file: Union[str, Path, BufferedReader],
        *,
        name: Optional[str] = None,
        workspace: Optional[str] = None,
        overwrite: bool = False,
    ) -> str:
        """Uploads a style.

        Note:
            The `name` parameter must be provided if the `file` argument is not a file path.

        Note:
            If overwriting a style, you must provide the `style` name.

        Args:
            file: The path to the file to upload.
            name: Optional. The name of the style. If not provided, it will be inferred from the filename.
            workspace: Optional. The name of the workspace.
            overwrite: Optional. Whether to overwrite the style if it already exists. Defaults to False.

        Returns:
            Success message.

        Example:
            To upload a style from a local SLD file:

            ```python
            file_path = "path/to/my_style.sld" # Or "path/to/my_style.zip"
            geoserver.upload_style(file=file_path, workspace="demo")

            # Open the file yourself
            with open(file_path, "rb") as f:
                geoserver.upload_style(file=f, workspace="demo")
            ```

            To overwrite an existing style with a new SLD file (or ZIP file):

            ```python
            file_path = "path/to/my_style.sld" # Or "path/to/my_style.zip"
            geoserver.upload_style(file=file_path, style="my_style", workspace="demo", overwrite=True)

            # Open the file yourself
            with open(file_path, "rb") as f:
                geoserver.upload_style(file=f, style="my_style", workspace="demo", overwrite=True)
            ```

        """
        method: Literal["post", "put"] = "put" if overwrite else "post"
        if overwrite and name is None:
            raise ValueError("The `style` argument must be provided when overwrite is `True`")

        # Upload from a zip file
        if zipfile.is_zipfile(file):
            headers = {"Content-Type": "application/zip"}
            url = f"{self.service_url}/rest/styles"
            if overwrite:
                url = f"{self.service_url}/rest/styles/{name}.zip"

            _ = self._request(method=method, url=url, file=file, headers=headers)
            return CREATED_MESSAGE

        # Upload from a single SLD file
        if name is None and isinstance(file, (str, Path)):
            name = Path(file).stem
        if name is None:
            raise ValueError("The `style` name must be provided, either as an argument or as the filename.")

        if not overwrite:
            body = f"<style><name>{name}</name><filename>{name}.sld</filename></style>"
            _ = self.create_style(body=body, workspace=workspace)

        body = file.read().decode("utf-8") if isinstance(file, BufferedReader) else Path(file).read_text()
        _ = self.update_style(name=name, body=body, workspace=workspace)
        return CREATED_MESSAGE

    def update_style(self, name: str, body: str, *, workspace: Optional[str] = None) -> str:
        """Updates a single style.

        Warning:
            This method only supports body in XML format.

        Args:
            name: The name of the style.
            body: The content of the updated style, in XML format.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/styles/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles/{name}"

        # Automatically determine the content type based on the SLD version
        pattern = r'StyledLayerDescriptor[^>]*version="([^"]*)"'
        match = re.search(pattern, body)
        if not match:
            raise ValueError("The SLD version could not be determined.")

        sld_version = match.group(1)

        content_type = "application/vnd.ogc.sld+xml"
        if sld_version == "1.1.0" or sld_version == "1.1":
            content_type = "application/vnd.ogc.se+xml"

        self._request(method="put", url=url, body=body, headers={"Content-Type": content_type})
        return UPDATED_MESSAGE

    def download_style(self, name: str, *, workspace: Optional[str] = None) -> str:
        """Downloads a single style.

        Args:
            name: The name of the style.
            workspace: Optional. The name of the workspace.

        Returns:
            The style content.
        """
        url = f"{self.service_url}/rest/styles/{name}.sld"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles/{name}.sld"

        response = self._request(method="get", url=url)
        return response.text

    def publish_style(self, layer: str, style: str, *, workspace: Optional[str] = None) -> str:
        """Publishes a style to a layer. This is equivalent to setting the default style for a layer,
        which will apply the style to the layer when it is rendered.

        Note:
            This method is equivalent to updating the layer with the default style.

        Args:
            layer: The name of the layer.
            style: The name of the style.
            workspace: Optional. The name of the workspace.

        Returns:
            Success message.

        Example:
            First, make sure the layer and style exist.
            Then, publish the style to the layer:

            ```python
            geoserver.publish_style(layer="my_layer", style="my_style", workspace="demo")
            ```

        """
        url = f"{self.service_url}/rest/layers/{layer}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{layer}"

        body = f"<layer><defaultStyle><name>{style}</name></defaultStyle></layer>"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_style(
        self, name: str, *, workspace: Optional[str] = None, purge: bool = False, recurse: bool = False
    ) -> str:
        """Deletes a single style.

        Args:
            name: The name of the style.
            workspace: Optional. The name of the workspace.
            purge: Optional. Whether to purge the style from the catalog. Defaults to False.
            recurse: Optional. Whether to delete references to the style. Defaults to False.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/styles/{name}"
        if workspace is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/styles/{name}"

        params = dict(purge=purge, recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    # Templates

    @overload
    def get_templates(
        self, *, workspace: Optional[str] = None, store: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_templates(
        self, *, workspace: Optional[str] = None, store: Optional[str] = None, format: Literal["xml"]
    ) -> str: ...

    def get_templates(
        self, *, workspace: Optional[str] = None, store: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Displays a list of all templates on the server.

        Args:
            workspace: Optional. The name of the workspace.
            store: Optional. The name of the store.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The templates.
        """
        if workspace is None and store is None:
            url = f"{self.service_url}/rest/templates.{format}"
        elif workspace is not None and store is None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/templates.{format}"
        elif workspace is not None and store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{store}/templates.{format}"
        else:
            raise ValueError("A workspace must be provided if a store is provided.")

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def get_template(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        data_store: Optional[str] = None,
        feature_type: Optional[str] = None,
        coverage_store: Optional[str] = None,
        coverage: Optional[str] = None,
    ) -> str:
        """Displays a list of all templates on the server.

        Args:
            name: The name of the template.
            workspace: Optional. The name of the workspace.
            data_store: Optional. The name of the datastore.
            feature_type: Optional. The name of the featuretype.
            coverage_store: Optional. The name of the coveragestore.
            coverage: Optional. The name of the coverage.

        Returns:
            The templates.
        """
        if (
            workspace is None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/templates/{name}.ftl"
        if (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is not None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/featuretypes/{feature_type}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is not None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/coverages/{coverage}/templates/{name}.ftl"
        else:
            raise ValueError(
                f"Invalid combinations of workspace, store, and featuretype. Got {workspace}, {data_store}, and {feature_type}."
            )

        response = self._request(method="get", url=url)
        return response.json()

    def create_template(
        self,
        name: str,
        body: str,
        *,
        workspace: Optional[str] = None,
        data_store: Optional[str] = None,
        feature_type: Optional[str] = None,
        coverage_store: Optional[str] = None,
        coverage: Optional[str] = None,
    ) -> str:
        """Inserts or updates a single template registered for use in a workspace (example for GetFeatureInfo WMS operation).
        Overwrites any existing template with the same name and location.

        Args:
            name: The name of the template.
            body: The body of the request used to modify the template.
            workspace: Optional. The name of the workspace.
            data_store: Optional. The name of the datastore.
            feature_type: Optional. The name of the featuretype.
            coverage_store: Optional. The name of the coveragestore.
            coverage: Optional. The name of the coverage.

        Returns:
            Success message.
        """
        if (
            workspace is None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/templates/{name}.ftl"
        if (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is not None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/featuretypes/{feature_type}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is not None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/coverages/{coverage}/templates/{name}.ftl"
        else:
            raise ValueError(
                f"Invalid combinations of workspace, store, and featuretype. Got {workspace}, {data_store}, and {feature_type}."
            )

        headers = {"Content-Type": "text/plain"}
        self._request(method="put", url=url, body=body, headers=headers)
        return CREATED_MESSAGE

    def delete_template(
        self,
        name: str,
        *,
        workspace: Optional[str] = None,
        data_store: Optional[str] = None,
        feature_type: Optional[str] = None,
        coverage_store: Optional[str] = None,
        coverage: Optional[str] = None,
    ) -> str:
        """Deletes a single template registered for use on the server.

        Args:
            name: The name of the template.
            workspace: Optional. The name of the workspace.
            data_store: Optional. The name of the datastore.
            feature_type: Optional. The name of the featuretype.
            coverage_store: Optional. The name of the coveragestore.
            coverage: Optional. The name of the coverage.

        Returns:
            Success message.
        """
        if (
            workspace is None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/templates/{name}.ftl"
        if (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is not None
            and feature_type is not None
            and coverage_store is None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/datastores/{data_store}/featuretypes/{feature_type}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/templates/{name}.ftl"
        elif (
            workspace is not None
            and data_store is None
            and feature_type is None
            and coverage_store is not None
            and coverage is not None
        ):
            url = f"{self.service_url}/rest/workspaces/{workspace}/coveragestores/{coverage_store}/coverages/{coverage}/templates/{name}.ftl"
        else:
            raise ValueError(
                f"Invalid combinations of workspace, store, and featuretype. Got {workspace}, {data_store}, and {feature_type}."
            )

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # GeoServer XSLT transforms

    @overload
    def get_wfs_transforms(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wfs_transforms(self, *, format: Literal["xml"]) -> str: ...

    def get_wfs_transforms(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays a list of all the transforms information available on the server.

        Args:
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The XSLT transforms.

        Example:
            To get the list of all the transforms available on the server, you can use the following code:

            ```python
            geoserver.get_transforms()
            ```
        """
        url = f"{self.service_url}/rest/services/wfs/transforms.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_wfs_transform(
        self,
        body: Union[str, Dict[str, Any]],
        *,
        source_format: Optional[str] = None,
        output_format: Optional[str] = None,
        output_mime_type: Optional[str] = None,
        file_extension: Optional[str] = None,
    ) -> str:
        """Adds a new transform to the server.
        If the content type used is application/xml the server will assume a definition is being posted,
        and the XSLT will have to be uploaded separately using a PUT request with content type application/xslt+xml against the transformation resource.
        If the content type used is application/xslt+xml the server will assume the XSLT itself is being posted,
        and the name, sourceFormat, outputFormat, outputMimeType query parameters will be used to fill in the transform configuration instead.

        Args:
            body: The body of the request used to create the transform.

        Returns:
            Success message.

        Example:
            To add a new transform to the server, you can use the following code:

            ```python
            body = \"\"\"
            <transform>
                <name>test</name>
                <sourceFormat>GML2</sourceFormat>
                <outputFormat>text/xml</outputFormat>
                <outputMimeType>text/xml</outputMimeType>
                <fileExtension>xml</fileExtension>
            </transform>
            \"\"\"

            geoserver.create_transform(body)
            ```
        """
        url = f"{self.service_url}/rest/services/wfs/transforms"
        params = dict(
            sourceFormat=source_format,
            outputFormat=output_format,
            outputMimeType=output_mime_type,
            fileExtension=file_extension,
        )
        self._request(method="post", url=url, body=body, params=params)
        return CREATED_MESSAGE

    @overload
    def get_wfs_transform(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wfs_transform(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_wfs_transform(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves a single transformation.

        Args:
            name: The name of the transform.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The transform.

        Example:
            To get a single transformation, you can use the following code:

            ```python
            geoserver.get_transform(transform="test1")
            ```
        """
        url = f"{self.service_url}/rest/services/wfs/transforms/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wfs_transform(self, name: str, body: Union[str, Dict[str, Any]]) -> str:
        """Modifies a single transform.

        Args:
            name: The name of the transform.
            body: The body of the request used to modify the transform.

        Returns:
            Success message.

        Example:
            To update a single transformation, you can use the following code:

            ```python
            body = \"\"\"
            <transform>
                <name>test1</name>
                <sourceFormat>text/xml; subtype=gml/2.1.2</sourceFormat>
                <outputFormat>text/html</outputFormat>
                <xslt>test1.xslt</xslt>
            </transform>
            \"\"\"

            geoserver.update_transform(transform="test1", body=body)
            ```
        """
        url = f"{self.service_url}/rest/services/wfs/transforms/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wfs_transform(self, name: str) -> str:
        """Deletes a single transform.

        Args:
            name: The name of the transform.

        Returns:
            Success message.

        Example:
            To remove a single transformation, you can use the following code:

            ```python
            geoserver.delete_transform(transform="test1")
            ```
        """
        url = f"{self.service_url}/rest/services/wfs/transforms/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # WMS Layers

    @overload
    def get_wms_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_wms_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_wms_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves the WMS layers available on the server.

        Args:
            workspace: The name of the workspace.
            store: Optional. Name of the wms store.
            list: Optional. Set `list=available` to see all possible layers in the store, not just ones currently published.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMS layers.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmslayers.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{store}/wmslayers.{format}"

        params = dict(list=list)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def create_wms_layer(self, body: Union[str, Dict[str, Any]], *, workspace: str, store: Optional[str] = None) -> str:
        """Creates a new WMS layer.

        Args:
            workspace: The name of the workspace.
            body: The body of the request used to create the WMS layer.
            store: Optional. Name of the wms store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmslayers"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{store}/wmslayers"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_wms_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_wms_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_wms_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves a single WMS layer.

        Args:
            name: The name of the wms layer.
            workspace: The name of the workspace.
            store: Optional. Name of the wms store.
            quiet_on_not_found: Optional. When set to "true", will not log an exception when the style is not present.
                The 404 status code will still be returned.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMS layer.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmslayers/{name}.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{store}/wmslayers/{name}.{format}"

        params = dict(quietOnNotFound=quiet_on_not_found)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def update_wms_layer(
        self,
        name: str,
        body: Union[str, Dict[str, Any]],
        *,
        workspace: str,
        store: Optional[str] = None,
        calculate: Optional[List[str]] = None,
    ) -> str:
        """Modifies a single WMS layer.

        Args:
            name: The name of the layer.
            body: The body of the request used to modify the WMS layer.
            workspace: The name of the workspace.
            calculate: Specifies whether to recalculate any bounding boxes for a wms layer.
                Some properties are automatically recalculated when necessary.
                In particular, the native bounding box is recalculated when the projection or projection policy are changed,
                and the lat/lon bounding box is recalculated when the native bounding box is recalculated,
                or when a new native bounding box is explicitly provided in the request.
                (The native and lat/lon bounding boxes are not automatically recalculated when they are explicitly included in the request.)
                In addition, the client may explicitly request a fixed set of fields to calculate,
                by including a comma-separated list of their names in the recalculate parameter.
                The empty parameter "recalculate=" is useful avoid slow recalculation when operating against large datasets
                as "recalculate=" avoids calculating any fields, regardless of any changes to projection, projection policy, etc.
                The nativebbox parameter "recalculate=nativebbox" is used recalculates the native bounding box,
                while avoiding recalculating the lat/lon bounding box. Recalculate parameters can be used in together -
                "recalculate=nativebbox,latlonbbox" can be used after a bulk import to
                recalculates both the native bounding box and the lat/lon bounding box.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmslayers/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{store}/wmslayers/{name}"

        params = dict(calculate=calculate)
        self._request(method="put", url=url, body=body, params=params)
        return UPDATED_MESSAGE

    def delete_wms_layer(self, name: str, *, workspace: str, store: Optional[str] = None, recurse: bool = False) -> str:
        """Deletes a single WMS layer.

        Args:
            name: The name of the layer.
            workspace: The name of the workspace.
            recurse: Recursively deletes all layers referenced by the specified wmslayer.
                A request with `recurse=false` will fail if any layers reference the wmslayer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmslayers/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{store}/wmslayers/{name}"

        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    # WMS Stores

    @overload
    def get_wms_stores(self, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wms_stores(self, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_wms_stores(self, *, workspace: str, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the WMS stores available on the server.

        Args:
            workspace: The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMS stores.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_wms_store(self, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Creates a new WMS store.

        Args:
            body: The body of the request used to create the WMS store.
            workspace: The name of the workspace.

        Returns:
            Success message.

        Example:
            To add a new WMS store to the server, you can use the following code:

            ```python
            body = \"\"\"
            <wmsStore>
                <name>remote</name>
                <capabilitiesUrl>http://demo.geoserver.org/geoserver/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities</capabilitiesUrl>
            </wmsStore>
            \"\"\"

            geoserver.create_wms_store(workspace="test", body=body)
            ```
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_wms_store(self, name: str, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wms_store(self, name: str, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_wms_store(
        self, name: str, *, workspace: str, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves a single WMS store.

        Args:
            name: The name of the WMS store.
            workspace: The name of the workspace.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMS store.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wms_store(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Modifies a single WMS store.

        Args:
            name: The name of the WMS store.
            workspace: The name of the workspace.
            body: The body of the request used to modify the WMS store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wms_store(self, name: str, *, workspace: str) -> str:
        """Deletes a single WMS store.

        Args:
            name: The name of the WMS store.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmsstores/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # WMTS Layers

    @overload
    def get_wmts_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_wmts_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_wmts_layers(
        self,
        *,
        workspace: str,
        store: Optional[str] = None,
        list: Optional[Literal["available"]] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves the WMTS layers available on the server.

        Args:
            workspace: The name of the workspace.
            store: Name of the wmts store.
            list: Set `list=available` to see all possible layers in the store, not just ones currently published.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMTS layers.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers.{format}"

        params = dict(list=list)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def wmts_layer_exists(self, name: str, *, workspace: str, store: Optional[str] = None) -> bool:
        """Check if a WMTS layer exists.

        Args:
            name: The name of the layer.
            workspace: The name of the workspace.
            store: Name of the wmts store.

        Returns:
            True if the WMTS layer exists, False otherwise.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}.xml"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers/{name}.xml"

        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_wmts_layer(
        self, body: Union[str, Dict[str, Any]], *, workspace: str, store: Optional[str] = None
    ) -> str:
        """Creates a new WMTS layer.

        Args:
            body: The body of the request used to create the WMTS layer.
            workspace: The name of the workspace.
            store: Name of the wmts store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_wmts_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_wmts_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["xml"],
    ) -> str: ...

    def get_wmts_layer(
        self,
        name: str,
        *,
        workspace: str,
        store: Optional[str] = None,
        quiet_on_not_found: bool = False,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves a single WMTS layer.

        Args:
            name: The name of the layer.
            workspace: The name of the workspace.
            store: Optional. Name of the wmts store.
            quiet_on_not_found: Optional. When set to "true", will not log an exception when the style is not present.
                The 404 status code will still be returned.
            format: Optional. The format of the response. It can be either "json" or "xml". Defaults to "json".

        Returns:
            The WMTS layer.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}.{format}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers/{name}.{format}"

        params = dict(quietOnNotFound=quiet_on_not_found)
        response = self._request(method="get", url=url, params=params)
        return response.json() if format == "json" else response.text

    def update_wmts_layer(
        self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str, store: Optional[str] = None
    ) -> str:
        """Modifies a single WMTS layer.

        Args:
            name: The name of the layer.
            body: The body of the request used to modify the WMTS layer.
            workspace: The name of the workspace.
            store: Name of the wmts store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers/{name}"

        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wmts_layer(
        self, name: str, *, workspace: str, store: Optional[str] = None, recurse: bool = False
    ) -> str:
        """Deletes a single WMTS layer.

        Args:
            name: The name of the layer.
            workspace: The name of the workspace.
            store: Name of the wmts store.
            recurse: Recursively deletes all layers referenced by the specified wmtslayer.
                A request with `recurse=false` will fail if any layers reference the wmtslayer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/layers/{name}"
        if store is not None:
            url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{store}/layers/{name}"

        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    # WMTS Stores

    @overload
    def get_wmts_stores(self, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wmts_stores(self, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_wmts_stores(self, *, workspace: str, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the WMTS stores available on the server.

        Args:
            workspace: The name of the workspace.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The WMTS stores.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def wmts_store_exists(self, name: str, *, workspace: str) -> bool:
        """Checks if a WMTS store exists on the server.

        Args:
            name: The name of the WMTS store.
            workspace: The name of the workspace.

        Returns:
            True if the WMTS store exists, False otherwise.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{name}.xml"
        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_wmts_store(self, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Creates a new WMTS store.

        Args:
            body: The body of the request used to create the WMTS store.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    @overload
    def get_wmts_store(self, name: str, *, workspace: str, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_wmts_store(self, name: str, *, workspace: str, format: Literal["xml"]) -> str: ...

    def get_wmts_store(
        self, name: str, *, workspace: str, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves a single WMTS store.

        Args:
            name: The name of the WMTS store.
            workspace: The name of the workspace.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The WMTS store.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_wmts_store(self, name: str, body: Union[str, Dict[str, Any]], *, workspace: str) -> str:
        """Modifies a single WMTS store.

        Args:
            name: The name of the WMTS store.
            body: The body of the request used to modify the WMTS store.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_wmts_store(self, name: str, *, workspace: str) -> str:
        """Deletes a single WMTS store.

        Args:
            name: The name of the WMTS store.
            workspace: The name of the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{workspace}/wmtsstores/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Workspaces

    @overload
    def get_workspaces(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_workspaces(self, *, format: Literal["xml"]) -> str: ...

    def get_workspaces(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays a list of all workspaces on the server.

        Args:
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The workspaces.
        """
        url = f"{self.service_url}/rest/workspaces.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def workspace_exists(self, name: str) -> bool:
        """Checks if a workspace exists on the server.

        Args:
            name: The name of the workspace.

        Returns:
            True if the workspace exists, False otherwise.
        """
        url = f"{self.service_url}/rest/workspaces/{name}.xml"
        response = self._request(method="head", url=url, ignore=[404])
        return response.status_code == 200

    def create_workspace(self, body: Union[str, Dict[str, Any]]) -> str:
        """Creates a new workspace.

        Args:
            body: The body of the request used to create the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    def create_workspace_from_name(self, name: str) -> str:
        """Shortcut to create a new workspace from a name.

        Args:
            name: The name of the workspace.

        Returns:
            Success message.
        """
        body = {"workspace": {"name": name}}
        return self.create_workspace(body=body)

    @overload
    def get_workspace(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_workspace(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_workspace(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Displays a single workspace on the server.

        Args:
            name: The name of the workspace.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The workspace.
        """
        url = f"{self.service_url}/rest/workspaces/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_workspace(self, name: str, body: Union[str, Dict[str, Any]]) -> str:
        """Modifies a single workspace.

        Args:
            name: The name of the workspace.
            body: The body of the request used to modify the workspace.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{name}"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_workspace(self, name: str, *, recurse: bool = False) -> str:
        """Deletes a single workspace.

        Args:
            name: The name of the workspace.
            recurse: Optional. Recursively deletes all resources in the workspace. Defaults to False.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/workspaces/{name}"
        params = dict(recurse=recurse)
        self._request(method="delete", url=url, params=params)
        return DELETED_MESSAGE

    # User Group

    @overload
    def get_users(
        self, *, service: Optional[str] = None, group: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_users(
        self, *, service: Optional[str] = None, group: Optional[str] = None, format: Literal["xml"]
    ) -> str: ...

    def get_users(
        self, *, service: Optional[str] = None, group: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Query all users in the default user/group service.

        Args:
            service: Optional. The name of the user/group service.
            group: Optional. The name of the group.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The users.
        """
        if service is None and group is None:
            url = f"{self.service_url}/rest/security/usergroup/users.{format}"
        elif service is not None and group is None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/users.{format}"
        elif service is None and group is not None:
            url = f"{self.service_url}/rest/security/usergroup/group/{group}/users.{format}"
        else:
            raise ValueError("Invalid combination of service and group.")

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_user(self, body: Union[str, Dict[str, Any]], *, service: Optional[str] = None) -> str:
        """Add a new user to the default user/group service.

        Args:
            body: The body of the request used to create the user.

        Returns:
            Success message.

        Example:
            To add a new user to the default user/group service, you can use the following code:

            ```python
            body = {
                "userName": "user",
                "password": "password",
                "enabled": "true",
            }
            geoserver.create_user(body=body)
            ```
        """
        url = f"{self.service_url}/rest/security/usergroup/users"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/users"

        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    def update_user(self, name: str, body: Union[str, Dict[str, Any]], *, service: Optional[str] = None) -> str:
        """Update an existing user in the default user/group service.

        Args:
            name: The name of the user.
            body: The body of the request used to modify the user.
            service: The name of the user/group service.

        Returns:
            Success message.

        Example:
            To update an existing user in the default user/group service, you can use the following code:

            ```python
            body = \"\"\"
            <user>
                <userName>user</userName>
                <password>password</password>
                <enabled>true</enabled>
            </user>
            \"\"\"

            geoserver.update_user("my_user", body=body)
            ```
        """
        url = f"{self.service_url}/rest/security/usergroup/user/{name}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/user/{name}"

        self._request(method="post", url=url, body=body)
        return UPDATED_MESSAGE

    def delete_user(self, name: str, *, service: Optional[str] = None) -> str:
        """Remove an existing user from the default user/group service.

        Args:
            name: The name of the user.
            service: The name of the user/group service.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/usergroup/user/{name}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/user/{name}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    @overload
    def get_user_groups(
        self, *, user: str, service: Optional[str] = None, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_user_groups(self, *, user: str, service: Optional[str] = None, format: Literal["xml"]) -> str: ...

    def get_user_groups(
        self, *, user: str, service: Optional[str] = None, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Query all groups in the default user/group service.

        Args:
            user: The name of the user.
            service: Optional. The name of the user/group service.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The groups.
        """
        url = f"{self.service_url}/rest/security/usergroup/user/{user}/groups.{format}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/user/{user}/groups.{format}"

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def associate_user(self, user: str, group: str, *, service: Optional[str] = None) -> str:
        """Associate a user with a group in the default user/group service.

        Args:
            user: The name of the user.
            group: The name of the group.
            service: The name of the user/group service.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/usergroup/user/{user}/group/{group}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/user/{user}/group/{group}"

        self._request(method="post", url=url)
        return OK_MESSAGE

    def disassociate_user(self, user: str, group: str, *, service: Optional[str] = None) -> str:
        """Remove a user from a group in the default user/group service.

        Args:
            user: The name of the user.
            group: The name of the group.
            service: The name of the user/group service.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/usergroup/user/{user}/group/{group}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/user/{user}/group/{group}"

        self._request(method="delete", url=url)
        return OK_MESSAGE

    def create_user_group(self, name: str, *, service: Optional[str] = None) -> str:
        """Add a new group to the default user/group service.

        Args:
            name: The name of the group.
            service: The name of the user/group service.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/usergroup/group/{name}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/group/{name}"

        self._request(method="post", url=url)
        return OK_MESSAGE

    def delete_user_group(self, name: str, *, service: Optional[str] = None) -> str:
        """Remove a group from the default user/group service.

        Args:
            name: The name of the group.
            service: The name of the user/group service.

        Returns:
            Success message.

        Example:
            To remove a group from the default user/group service, you can use the following code:

            ```python
            geoserver.delete_group(group="group")
            ```
        """
        url = f"{self.service_url}/rest/security/usergroup/group/{name}"
        if service is not None:
            url = f"{self.service_url}/rest/security/usergroup/service/{service}/group/{name}"

        self._request(method="delete", url=url)
        return OK_MESSAGE

    # Roles

    @overload
    def get_roles(
        self,
        *,
        service: Optional[str] = None,
        group: Optional[str] = None,
        user: Optional[str] = None,
        format: Literal["json"] = "json",
    ) -> Dict[str, Any]: ...

    @overload
    def get_roles(
        self,
        *,
        service: Optional[str] = None,
        group: Optional[str] = None,
        user: Optional[str] = None,
        format: Literal["xml"],
    ) -> str: ...

    def get_roles(
        self,
        *,
        service: Optional[str] = None,
        group: Optional[str] = None,
        user: Optional[str] = None,
        format: Literal["json", "xml"] = "json",
    ) -> Union[str, Dict[str, Any]]:
        """Query all roles in the default user/group service.

        Args:
            service: Optional. The name of the user/group service.
            group: Optional. The name of the group.
            user: Optional. The name of the user.
            format: Optional. The format of the response. Can be either "json" or "xml".

        Returns:
            The roles.

        Example:
            To get all roles in the default user/group service, you can use the following code:

            ```python
            geoserver.get_roles()
            ```
        """
        if service is None and group is None and user is None:
            url = f"{self.service_url}/rest/security/roles.{format}"
        elif service is not None and group is None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}.{format}"
        elif service is None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/group/{group}.{format}"
        elif service is not None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/group/{group}.{format}"
        elif service is not None and group is None and user is not None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/user/{user}.{format}"
        else:
            raise ValueError("Invalid combination of service, group and user.")

        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def create_role(self, name: str) -> str:
        """Add a new role to the default user/group service.

        Args:
            name: The name of the role.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/roles/role/{name}"

        self._request(method="post", url=url)
        return CREATED_MESSAGE

    def delete_role(self, name: str) -> str:
        """Remove a role from the default user/group service.

        Args:
            name: The name of the role.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/rest/security/roles/role/{name}"

        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    def associate_role(
        self, role: str, *, service: Optional[str] = None, group: Optional[str] = None, user: Optional[str] = None
    ) -> str:
        """Associate a user with a role in the default user/group service.

        Args:
            role: The name of the role.
            service: The name of the user/group service.
            group: The name of the group.
            user: The name of the user.

        Returns:
            Success message.

        Example:
            To associate a user with a role in the default user/group service, you can use the following code:

            ```python
            geoserver.associate_role(role="ROLE_ADMIN", user="admin")
            ```
        """
        if service is not None and group is None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}"
        elif service is None and group is None and user is not None:
            url = f"{self.service_url}/rest/security/roles/role/{role}/user/{user}"
        elif service is None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/role/{role}/group/{group}"
        elif service is not None and group is None and user is not None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}/user/{user}"
        elif service is not None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}/group/{group}"
        else:
            raise ValueError("Invalid combination of service, group and user.")

        self._request(method="post", url=url)
        return OK_MESSAGE

    def disassociate_role(
        self, role: str, *, service: Optional[str] = None, group: Optional[str] = None, user: Optional[str] = None
    ) -> str:
        """Disassociate a user with a role in the default user/group service.

        Args:
            role: The name of the role.
            service: The name of the user/group service.
            group: The name of the group.
            user: The name of the user.

        Returns:
            Success message.

        Example:
            To disassociate a user from a role in the default user/group service, you can use the following code:

            ```python
            geoserver.disassociate_role(role="ROLE_ADMIN", user="admin")
            ```
        """
        if service is not None and group is None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}"
        elif service is None and group is None and user is not None:
            url = f"{self.service_url}/rest/security/roles/role/{role}/user/{user}"
        elif service is None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/role/{role}/group/{group}"
        elif service is not None and group is None and user is not None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}/user/{user}"
        elif service is not None and group is not None and user is None:
            url = f"{self.service_url}/rest/security/roles/service/{service}/role/{role}/group/{group}"
        else:
            raise ValueError("Invalid combination of service, group and user.")

        self._request(method="delete", url=url)
        return OK_MESSAGE
