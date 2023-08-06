# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.384.10

from __future__ import annotations

import io
import json
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class DataFileUploadResponse:
    """

    Attributes
    ----------
    createdDate: str
      The date that the uploaded file was created.
    id: str
      The ID for the uploaded file.
    name: str
      The name of the uploaded file.
    ownerId: str
      The 'owner' of a file is the user who last uploaded the file's content.
    size: int
      The size of the uploaded file, in bytes.
    appId: str
      If this file is bound to the lifecycle of a specific app, this is the ID of this app.
    modifiedDate: str
      The date that the updated file was last modified.
    spaceId: str
      If the file was uploaded to a team space, this is the ID of that space.
    """

    createdDate: str = None
    id: str = None
    name: str = None
    ownerId: str = None
    size: int = None
    appId: str = None
    modifiedDate: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "createdDate" in kvargs:
            if (
                type(kvargs["createdDate"]).__name__
                is self_.__annotations__["createdDate"]
            ):
                self_.createdDate = kvargs["createdDate"]
            else:
                self_.createdDate = kvargs["createdDate"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "size" in kvargs:
            if type(kvargs["size"]).__name__ is self_.__annotations__["size"]:
                self_.size = kvargs["size"]
            else:
                self_.size = kvargs["size"]
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ is self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "modifiedDate" in kvargs:
            if (
                type(kvargs["modifiedDate"]).__name__
                is self_.__annotations__["modifiedDate"]
            ):
                self_.modifiedDate = kvargs["modifiedDate"]
            else:
                self_.modifiedDate = kvargs["modifiedDate"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_connection(self) -> ConnectionsResponse:
        """
        Get the built-in connection used by the engine to load/write data files given a connection ID.

        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/data-files/connections/{id}".replace("{id}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = ConnectionsResponse(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self) -> None:
        """
        Delete the specified data file.

        Parameters
        ----------
        """

        self.auth.rest(
            path="/data-files/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(
        self,
        File: io.BufferedReader,
        appId: str = None,
        connectionId: str = None,
        name: str = None,
        sourceId: str = None,
        tempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Re-upload an existing data file.

        Parameters
        ----------
        """

        files_dict = {}
        files_dict["File"] = File

        Json_dict = {}
        if appId is not None:
            Json_dict["appId"] = appId
        if connectionId is not None:
            Json_dict["connectionId"] = connectionId
        if name is not None:
            Json_dict["name"] = name
        if sourceId is not None:
            Json_dict["sourceId"] = sourceId
        if tempContentFileId is not None:
            Json_dict["tempContentFileId"] = tempContentFileId
        files_dict["Json"] = (None, json.dumps(Json_dict))

        response = self.auth.rest(
            path="/data-files/{id}".replace("{id}", self.id),
            method="PUT",
            params={},
            data=None,
            files=files_dict,
        )
        self.__init__(**response.json())
        return self

    def change_owner(self, data: ChangeDataFileOwnerRequest) -> None:
        """
        Change the owner of an existing data file.
        This is primarily an admin type of operation. In general, the owner of a data file is implicitly set as
        part of a data file upload. For data files that reside in a personal space, changing the owner has the
        effect of moving the data file to the new owner's personal space.

        Parameters
        ----------
        data: ChangeDataFileOwnerRequest
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/data-files/{id}/actions/change-owner".replace("{id}", self.id),
            method="POST",
            params={},
            data=data,
        )

    def change_space(self, data: ChangeDataFileSpaceRequest) -> None:
        """
        Change the space that an existing data file resides in.
        This is to allow for a separate admin type of operation that is more global in terms of access in cases
        where admin users may not explicitly have been granted full access to a given space within the declared
        space-level permissions. If the space ID is set to null, then the datafile will end up residing in the
        personal space of the user who is the owner of the file.

        Parameters
        ----------
        data: ChangeDataFileSpaceRequest
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/data-files/{id}/actions/change-space".replace("{id}", self.id),
            method="POST",
            params={},
            data=data,
        )


@dataclass
class BatchChangeSpaceItem:
    """

    Attributes
    ----------
    id: str
      The ID of the data file whose space will be changed.
    spaceId: str
      The ID of the new space. Passing in a null will result in the data file being moved to the user's
      personal space.
    """

    id: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class BatchDeleteItem:
    """

    Attributes
    ----------
    id: str
      The ID of the data file to delete.
    """

    id: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChangeDataFileOwnerRequest:
    """

    Attributes
    ----------
    ownerId: str
      The ID of the new owner.
    """

    ownerId: str = None

    def __init__(self_, **kvargs):
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ChangeDataFileSpaceRequest:
    """

    Attributes
    ----------
    spaceId: str
      The ID of the space. If null, this data file will be moved to the user's personal space.
    """

    spaceId: str = None

    def __init__(self_, **kvargs):
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConnectionsResponse:
    """

    Attributes
    ----------
    connectStatement: str
      The connect statement that will be passed to the connector when invoked.
    id: str
    name: str
      The name of the connection.
    type: str
      The type of the connection.
    spaceId: str
      The team space that the given connection is associated with. If null, the connection is not associated
      with any specific team space.
    """

    connectStatement: str = None
    id: str = None
    name: str = None
    type: str = None
    spaceId: str = None

    def __init__(self_, **kvargs):
        if "connectStatement" in kvargs:
            if (
                type(kvargs["connectStatement"]).__name__
                is self_.__annotations__["connectStatement"]
            ):
                self_.connectStatement = kvargs["connectStatement"]
            else:
                self_.connectStatement = kvargs["connectStatement"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileBatchChangeSpaceRequest:
    """
    Specifies the list of data file change space operations in a single batch.

    Attributes
    ----------
    change-space: list[BatchChangeSpaceItem]
      The list of data files to delete.
    """

    change_space: list[BatchChangeSpaceItem] = None

    def __init__(self_, **kvargs):
        if "change-space" in kvargs:
            if (
                type(kvargs["change-space"]).__name__
                is self_.__annotations__["change-space"]
            ):
                self_.change_space = kvargs["change-space"]
            else:
                self_.change_space = [
                    BatchChangeSpaceItem(**e) for e in kvargs["change-space"]
                ]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DataFileBatchDeleteRequest:
    """
    Specifies the list of data files to be deleted in a single batch.

    Attributes
    ----------
    delete: list[BatchDeleteItem]
      The list of data files to delete.
    """

    delete: list[BatchDeleteItem] = None

    def __init__(self_, **kvargs):
        if "delete" in kvargs:
            if type(kvargs["delete"]).__name__ is self_.__annotations__["delete"]:
                self_.delete = kvargs["delete"]
            else:
                self_.delete = [BatchDeleteItem(**e) for e in kvargs["delete"]]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetConnectionsResponse:
    """

    Attributes
    ----------
    data: list[ConnectionsResponse]
    links: LinksResponse
    """

    data: list[ConnectionsResponse] = None
    links: LinksResponse = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ConnectionsResponse(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = LinksResponse(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GetDataFileInfosResponse:
    """

    Attributes
    ----------
    data: list[DataFileUploadResponse]
    links: LinksResponse
    """

    data: list[DataFileUploadResponse] = None
    links: LinksResponse = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [DataFileUploadResponse(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = LinksResponse(**kvargs["links"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinkResponse:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):
        if "href" in kvargs:
            if type(kvargs["href"]).__name__ is self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LinksResponse:
    """

    Attributes
    ----------
    next: LinkResponse
    prev: LinkResponse
    self: LinkResponse
    """

    next: LinkResponse = None
    prev: LinkResponse = None
    self: LinkResponse = None

    def __init__(self_, **kvargs):
        if "next" in kvargs:
            if type(kvargs["next"]).__name__ is self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = LinkResponse(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ is self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = LinkResponse(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ is self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = LinkResponse(**kvargs["self"])
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class QuotaResponse:
    """

    Attributes
    ----------
    allowedExtensions: list[str]
      The allowed file extensions on files that are uploaded.
    allowedInternalExtensions: list[str]
      The allowed file extensions for files that are only used internally by the system (and thus not typically
      shown to end users).
    maxFileSize: int
      Maximum allowable size of an uploaded file.
    maxLargeFileSize: int
      Maximum allowable size for a single uploaded large data file (in bytes). This is a file that was indirectly
      uploaded using the temp content service chunked upload capability.
    maxSize: int
      The maximum aggregate size of all files uploaded by a given user.
    size: int
      The current aggregate size of all files uploaded by a given user. If the current aggregate size is greater
      than the maximum aggregate size, this is a quota violation.
    """

    allowedExtensions: list[str] = None
    allowedInternalExtensions: list[str] = None
    maxFileSize: int = None
    maxLargeFileSize: int = None
    maxSize: int = None
    size: int = None

    def __init__(self_, **kvargs):
        if "allowedExtensions" in kvargs:
            if (
                type(kvargs["allowedExtensions"]).__name__
                is self_.__annotations__["allowedExtensions"]
            ):
                self_.allowedExtensions = kvargs["allowedExtensions"]
            else:
                self_.allowedExtensions = kvargs["allowedExtensions"]
        if "allowedInternalExtensions" in kvargs:
            if (
                type(kvargs["allowedInternalExtensions"]).__name__
                is self_.__annotations__["allowedInternalExtensions"]
            ):
                self_.allowedInternalExtensions = kvargs["allowedInternalExtensions"]
            else:
                self_.allowedInternalExtensions = kvargs["allowedInternalExtensions"]
        if "maxFileSize" in kvargs:
            if (
                type(kvargs["maxFileSize"]).__name__
                is self_.__annotations__["maxFileSize"]
            ):
                self_.maxFileSize = kvargs["maxFileSize"]
            else:
                self_.maxFileSize = kvargs["maxFileSize"]
        if "maxLargeFileSize" in kvargs:
            if (
                type(kvargs["maxLargeFileSize"]).__name__
                is self_.__annotations__["maxLargeFileSize"]
            ):
                self_.maxLargeFileSize = kvargs["maxLargeFileSize"]
            else:
                self_.maxLargeFileSize = kvargs["maxLargeFileSize"]
        if "maxSize" in kvargs:
            if type(kvargs["maxSize"]).__name__ is self_.__annotations__["maxSize"]:
                self_.maxSize = kvargs["maxSize"]
            else:
                self_.maxSize = kvargs["maxSize"]
        if "size" in kvargs:
            if type(kvargs["size"]).__name__ is self_.__annotations__["size"]:
                self_.size = kvargs["size"]
            else:
                self_.size = kvargs["size"]
        for k, v in kvargs.items():
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class DataFiles:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_data_files(
        self,
        allowInternalFiles: bool = None,
        appId: str = None,
        connectionId: str = None,
        limit: int = 20,
        name: str = None,
        ownerId: str = None,
        page: str = None,
        sort: str = None,
        max_items: int = 20,
    ) -> ListableResource[DataFileUploadResponse]:
        """
        Get descriptive info for the specified data files.


        allowInternalFiles: bool
          If set to false, do not return data files with internal extensions else return all the data files.

        appId: str
          Only return files scoped to the specified app. If this parameter is not specified, only files that are not
          scoped to any app are returned. "*" implies all app-scoped files are returned.

        connectionId: str
          Return files that reside in the space referenced by the specified DataFiles connection. If this parameter
          is not specified, the user's personal space is implied.

        limit: int
          If present, the maximum number of data files to return.

        name: str
          Filter the list of files returned to the given file name.

        ownerId: str
          If present, fetch the data files for the specified owner. If a connectionId is specified in this case, the
          returned list is constrained to the specified space. If connectionId is not specified, then all files owned
          by the specified user are returned regardless of the personal space that a given file resides in.

        page: str
          If present, the cursor that starts the page of data that is returned.

        sort: str
          The name of the field used to sort the result. By default, the sort order is ascending. Putting a '+' prefix on
          the sort field name explicitly indicates ascending sort order. A '-' prefix indicates a descending sort order.

        Parameters
        ----------
        allowInternalFiles: bool = None
        appId: str = None
        connectionId: str = None
        limit: int = 20
        name: str = None
        ownerId: str = None
        page: str = None
        sort: str = None
        """
        query_params = {}
        if allowInternalFiles is not None:
            query_params["allowInternalFiles"] = allowInternalFiles
        if appId is not None:
            query_params["appId"] = appId
        if connectionId is not None:
            query_params["connectionId"] = connectionId
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort

        response = self.auth.rest(
            path="/data-files",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=DataFileUploadResponse,
            auth=self.auth,
            path="/data-files",
            max_items=max_items,
            query_params=query_params,
        )

    def create(
        self,
        File: io.BufferedReader,
        name: str = None,
        appId: str = None,
        connectionId: str = None,
        sourceId: str = None,
        tempContentFileId: str = None,
    ) -> DataFileUploadResponse:
        """
        Upload a new data file.


        Parameters
        ----------
        """

        files_dict = {}
        files_dict["File"] = File

        Json_dict = {}
        if name is not None:
            Json_dict["name"] = name
        if appId is not None:
            Json_dict["appId"] = appId
        if connectionId is not None:
            Json_dict["connectionId"] = connectionId
        if sourceId is not None:
            Json_dict["sourceId"] = sourceId
        if tempContentFileId is not None:
            Json_dict["tempContentFileId"] = tempContentFileId
        files_dict["Json"] = (None, json.dumps(Json_dict))

        response = self.auth.rest(
            path="/data-files", method="POST", params={}, data=None, files=files_dict
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj

    def change_space(self, data: DataFileBatchChangeSpaceRequest) -> None:
        """
        Change the spaces that a set of existing data files reside in a a single batch.
        This is to allow for a separate admin type of operation that is more global in terms of access in cases
        where admin users may not explicitly have been granted full access to a given space within the declared
        space-level permissions. If the space ID is set to null, then the data file will end up residing in the
        personal space of the user who is the owner of the file.


        Parameters
        ----------
        data: DataFileBatchChangeSpaceRequest
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/data-files/actions/change-space",
            method="POST",
            params={},
            data=data,
        )

    def delete(self, data: DataFileBatchDeleteRequest) -> None:
        """
        Delete the specified set of data files as a single batch.


        Parameters
        ----------
        data: DataFileBatchDeleteRequest
        """

        try:
            data = asdict(data)
        except:
            data = data

        self.auth.rest(
            path="/data-files/actions/delete",
            method="POST",
            params={},
            data=data,
        )

    def get_connections(
        self,
        appId: str = None,
        limit: int = 20,
        name: str = None,
        page: str = None,
        personal: bool = None,
        sort: str = None,
        spaceId: str = None,
        max_items: int = 20,
    ) -> ListableResource[ConnectionsResponse]:
        """
        Get the list of built-in connections used by the engine to load/write data files.
        The non-filtered list contains a set of hardcoded connections, along with one connection per team space that
        the given user has access to.


        appId: str
          If present, get connections with connection strings that are scoped to the given app ID.

        limit: int
          If present, the maximum number of data file connection records to return.

        name: str
          If present, only return connections with the given name.

        page: str
          If present, the cursor that starts the page of data that is returned.

        personal: bool
          If true, only return the connections that access data in a personal space. Default is false.

        sort: str
          The name of the field used to sort the result. By default, the sort is ascending. Putting a '+' prefix on
          the sort field name explicitly indicates ascending sort order. A '-' prefix indicates a descending sort order.

        spaceId: str
          If present, only return the connection that accesses data files in the specified space.

        Parameters
        ----------
        appId: str = None
        limit: int = 20
        name: str = None
        page: str = None
        personal: bool = None
        sort: str = None
        spaceId: str = None
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if page is not None:
            query_params["page"] = page
        if personal is not None:
            query_params["personal"] = personal
        if sort is not None:
            query_params["sort"] = sort
        if spaceId is not None:
            query_params["spaceId"] = spaceId

        response = self.auth.rest(
            path="/data-files/connections",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ConnectionsResponse,
            auth=self.auth,
            path="/data-files/connections",
            max_items=max_items,
            query_params=query_params,
        )

    def get_quota(self) -> QuotaResponse:
        """
        Get quota information for the calling user.


        Parameters
        ----------
        """

        response = self.auth.rest(
            path="/data-files/quotas",
            method="GET",
            params={},
            data=None,
        )
        obj = QuotaResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> DataFileUploadResponse:
        """
        Get descriptive info for the specified data file.


        id: str
          The ID of the data file.

        Parameters
        ----------
        id: str
        """

        response = self.auth.rest(
            path="/data-files/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = DataFileUploadResponse(**response.json())
        obj.auth = self.auth
        return obj
