from typing import Union
from fastapi import HTTPException

from autoretouchlib.types import FileContentHash, OrganizationId, FileType


class MockStorage:
    def __init__(self):
        self.__storage = {}
        self.__real_uris = {}

    @staticmethod
    def __make_key(organization_id: OrganizationId, content_hash: FileContentHash) -> str:
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        return organization_id + "/origin/" + content_hash.get_value()

    def load(self, content_hash: Union[FileContentHash, str], organization_id: OrganizationId) -> bytes:
        try:
            return self.__storage[self.__make_key(organization_id, content_hash)]
        except KeyError:
            raise HTTPException(status_code=404)

    def store(self, blob: bytes, content_type: Union[FileType, str], organization_id: OrganizationId) \
            -> FileContentHash:
        if isinstance(content_type, str):
            content_type = FileType(content_type)
        content_hash = FileContentHash.from_bytes(blob)
        self.__storage[self.__make_key(organization_id, content_hash)] = blob
        return content_hash

    def uri_for(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str]) -> str:
        try:
            return self.__real_uris[self.__make_key(organization_id, content_hash)]
        except KeyError:
            raise HTTPException(status_code=404)

    def add_real_uri(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str], uri: str):
        self.__real_uris[self.__make_key(organization_id, content_hash)] = uri
