from typing import Any, Dict, Literal, Union, overload

from .base import Base
from .consts import CREATED_MESSAGE, DELETED_MESSAGE, UPDATED_MESSAGE


class GeoWebCache(Base):
    @overload
    def get_blob_stores(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_blob_stores(self, *, format: Literal["xml"]) -> str: ...

    def get_blob_stores(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the blob stores available on the server.

        Args:
            format: Optional. The format of the response.

        Returns:
            The blob stores.
        """
        url = f"{self.service_url}/gwc/rest/blobstores.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    @overload
    def get_blob_store(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_blob_store(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_blob_store(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves a single blob store.

        Args:
            name: The name of the blob store.
            format: Optional. The format of the response.

        Returns:
            The blob store.
        """
        url = f"{self.service_url}/gwc/rest/blobstores/{name}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def insert_blob_store(self, name: str, body: Union[str, Dict[str, Any]]) -> str:
        """Creates a new blob store.

        Args:
            name: The name of the blob store.
            body: The body of the request used to create the blob store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/blobstores/{name}.json"
        self._request(method="post", url=url, body=body)
        return CREATED_MESSAGE

    def delete_blob_store(self, name: str) -> str:
        """Deletes a single blob store.

        Args:
            name: The name of the blob store.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/blobstores/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Bounds

    @overload
    def get_layer_bounds(
        self, layer: str, srs: str, type: str, *, format: Literal["json"] = "json"
    ) -> Dict[str, Any]: ...

    @overload
    def get_layer_bounds(self, layer: str, srs: str, type: str, *, format: Literal["xml"]) -> str: ...

    def get_layer_bounds(
        self, layer: str, srs: str, type: str, *, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Retrieves the bounds for a layer.

        Args:
            layer: The name of the layer.
            srs: The srs projection used against the layer to find the bounds such as EPSG:4326.
            type: Accepts java as an extension.
            format: Optional. The format of the response.

        Returns:
            The bounds.
        """
        url = f"{self.service_url}/gwc/rest/bounds/{layer}/{srs}/{type}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # Disk Quota

    @overload
    def get_diskquota(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_diskquota(self, *, format: Literal["xml"]) -> str: ...

    def get_diskquota(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the disk quota settings.

        Args:
            format: Optional. The format of the response.

        Returns:
            The disk quota settings.
        """
        url = f"{self.service_url}/gwc/rest/diskquota.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_diskquota(self, body: Union[str, Dict[str, Any]]) -> str:
        """Modifies the disk quota settings.

        Args:
            body: The body of the request used to modify the disk quota settings.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/diskquota"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    @overload
    def filter_update(self, filter: str, update: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def filter_update(self, filter: str, update: str, *, format: Literal["xml"]) -> str: ...

    def filter_update(
        self, filter: str, update: str, *, format: Literal["json", "xml"] = "json"
    ) -> Union[str, Dict[str, Any]]:
        """Restfully updates the given filter with parameters provided in the xml or zip.

        Args:
            filter: The filter to use for the update.
            update: The update to apply.
            format: Optional. The format of the response.

        Returns:
            The response.
        """
        url = f"{self.service_url}/gwc/rest/filter/{filter}/update/{update}.{format}"
        response = self._request(method="post", url=url)
        return response.json() if format == "json" else response.text

    @overload
    def get_global_settings(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_global_settings(self, *, format: Literal["xml"]) -> str: ...

    def get_global_settings(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the global settings.

        Args:
            format: Optional. The format of the response.

        Returns:
            The global settings.
        """
        url = f"{self.service_url}/gwc/rest/global.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def update_global_settings(self, body: Union[str, Dict[str, Any]]) -> str:
        """Modifies the global settings.

        Args:
            body: The body of the request used to modify the global settings.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/global"
        self._request(method="put", url=url, body=body)
        return UPDATED_MESSAGE

    # Gridsets

    @overload
    def get_gridsets(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_gridsets(self, *, format: Literal["xml"]) -> str: ...

    def get_gridsets(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the gridsets available on the server.

        Args:
            format: Optional. The format of the response.

        Returns:
            The gridsets.
        """
        url = f"{self.service_url}/gwc/rest/gridsets.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    @overload
    def get_gridset(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_gridset(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_gridset(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves a single gridset.

        Args:
            name: The name of the gridset.
            format: Optional. The format of the response.

        Returns:
            The gridset.
        """
        url = f"{self.service_url}/gwc/rest/gridsets/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def insert_gridset(self, name: str, body: Union[str, Dict[str, Any]]) -> str:
        """Creates a new configured gridset on the server, or modifies an existing gridset.

        Args:
            name: The name of the gridset.
            body: The body of the request used to modify the gridset.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/gridsets/{name}"
        response = self._request(method="put", url=url, body=body)
        return response.text

    def delete_gridset(self, name: str) -> str:
        """Deletes a single gridset.

        Args:
            name: The name of the gridset.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/gridsets/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Layers

    @overload
    def get_layers(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_layers(self, *, format: Literal["xml"]) -> str: ...

    def get_layers(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the layers available on the server.

        Args:
            format: Optional. The format of the response.

        Returns:
            The layers.
        """
        url = f"{self.service_url}/gwc/rest/layers.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    @overload
    def get_layer(self, name: str, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_layer(self, name: str, *, format: Literal["xml"]) -> str: ...

    def get_layer(self, name: str, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves a single layer.

        Args:
            name: The name of the layer.
            format: Optional. The format of the response.

        Returns:
            The layer.
        """
        url = f"{self.service_url}/gwc/rest/layers/{name}.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    def insert_layer(self, name: str, body: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Creates a new layer on the server, or modifies an existing layer.

        Args:
            name: The name of the layer.
            body: The body of the request used to modify the layer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/layers/{name}"
        response = self._request(method="put", url=url, body=body)
        return response.json()

    def delete_layer(self, name: str) -> str:
        """Deletes a single layer.

        Args:
            name: The name of the layer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/layers/{name}"
        self._request(method="delete", url=url)
        return DELETED_MESSAGE

    # Mass Truncate

    @overload
    def get_masstruncate(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_masstruncate(self, *, format: Literal["xml"]) -> str: ...

    def get_masstruncate(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Returns xml containing the request type capabilities for mass truncation.

        Args:
            format: Optional. The format of the response.

        Returns:
            The mass truncate settings.
        """
        url = f"{self.service_url}/gwc/rest/masstruncate.{format}"
        headers = {"Accept": "application/xml"}
        response = self._request(method="get", url=url, headers=headers)
        return response.json() if format == "json" else response.text

    def create_masstruncate(self, *, request_type: str, layer: str) -> str:
        """Issues a mass truncate request based on the request type parameter.
        truncateLayer, will clear all caches associated with a named layer, including all permutations of gridset,
        parameter filter values, and image formats.

        Args:
            request_type: The type of request.
            layer: The name of the layer.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/masstruncate"
        params = dict(requestType=request_type, layer=layer)
        response = self._request(method="post", url=url, params=params)
        return response.text

    # Statistics

    @overload
    def get_statistics(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_statistics(self, *, format: Literal["xml"]) -> str: ...

    def get_statistics(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Retrieves the statistics for a layer or gridset.

        Args:
            format: Optional. The format of the response.

        Returns:
            The statistics.
        """
        url = f"{self.service_url}/gwc/rest/statistics.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # Reload

    def reload(self, body: str) -> str:
        """Reloads the GeoWebCache settings after making changes to the configuration.

        Args:
            body: The string value of the configuration ie. `reload_configuration=1`.

        Returns:
            Success message.
        """
        url = f"{self.service_url}/gwc/rest/reload"
        headers = {"Content-Type": "text/plain"}
        response = self._request(method="post", url=url, data=body, headers=headers)
        return response.text

    # Seed

    @overload
    def get_seed(self, *, format: Literal["json"] = "json") -> Dict[str, Any]: ...

    @overload
    def get_seed(self, *, format: Literal["xml"]) -> str: ...

    def get_seed(self, *, format: Literal["json", "xml"] = "json") -> Union[str, Dict[str, Any]]:
        """Query's and returns a json array of the status for all currently running task.
        The array contains a set of long in the following order:
        [tiles processed, total number of tiles to process, number of remaining tiles, Task ID, Task status].
        The returned task status will be one of -1 = ABORTED, 0 = PENDING, 1 = RUNNING, 2 = DONE

        Args:
            format: Optional. The format of the response.

        Returns:
            The seed settings.
        """
        url = f"{self.service_url}/gwc/rest/seed.{format}"
        response = self._request(method="get", url=url)
        return response.json() if format == "json" else response.text

    # TODO!

    # === Importer Extension ===
    # Imports
    # Imports (Tasks)
    # Imports (Transforms)
    # Imports (Data)

    # === Monitor Extension ===
    # Monitor

    # === XSLT Extension ===
    # Services WFS Transform
    # Services WFS Transform
