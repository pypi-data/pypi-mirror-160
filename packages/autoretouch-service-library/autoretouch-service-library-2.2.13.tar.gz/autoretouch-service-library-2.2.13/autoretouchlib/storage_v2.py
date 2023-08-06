import logging
import errno
import os
import io
import httpx

from fastapi import HTTPException
from typing import Union, Dict, List
from autoretouchlib.auth import get_id_token
from autoretouchlib.types import FileContentHash, OrganizationId, FileType


class Storage:

    def __init__(self):
        self.url = os.getenv("STORAGE_SERVICE_URL", "http://0.0.0.0:8180") + "/image/"
        self.__refresh_id_token()
        self.client = httpx.Client(http2=True, timeout=httpx.Timeout(None, read=300, write=300, connect=300))

    def __refresh_id_token(self):
        try:
            self.id_token = get_id_token(self.url)
        except RuntimeError:
            self.id_token = None

    def load(self, content_hash: Union[FileContentHash, str], organization_id: OrganizationId
             ) -> bytes:
        self.__refresh_id_token()
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        headers = {} if not self.id_token else {"Authorization": f"Bearer {self.id_token}"}
        params = {
            "organization_id": organization_id,
            "content_hash": content_hash.get_value()
        }
        response = self.client.get(self.url, params=params, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"could not load image from storage: {response.content.decode('utf-8')}")
        content_length = response.headers.get("Content-Length", response.headers.get("X-Content-Length"))
        if content_length is None:
            raise HTTPException(status_code=500,
                                detail=f"No content-length header received when requesting {organization_id}/{content_hash}")
        else:
            logging.debug(f"len(content): {len(response.content)}, content_length: {content_length}")
            if len(response.content) != int(content_length):
                raise HTTPException(status_code=500,
                                    detail=f"response was truncated: expected {int(content_length)} bytes, "
                                           f"received {len(response.content)} bytes")
        return response.content

    def store(self, blob: bytes, content_type: Union[FileType, str], organization_id: OrganizationId
              ) -> FileContentHash:
        self.__refresh_id_token()
        if isinstance(content_type, str):
            content_type = FileType(content_type)
        content_hash = FileContentHash.from_bytes(blob)

        headers = {} if not self.id_token else {"Authorization": f"Bearer {self.id_token}"}
        params = {
            "organization_id": organization_id,
            "content_hash": content_hash.get_value(),
            "content_type": content_type.value,
        }
        # check image exists
        response = self.client.head(self.url, params=params, headers=headers)
        if response.status_code in (200, 201):
            return content_hash
        try:
            response = self.client.post(self.url, params=params, content=io.BytesIO(blob), headers=headers)
            if response.status_code not in (200, 201):
                if response.status_code == 409:  # image exists already
                    return content_hash
                logging.warning(response.status_code, response.content.decode('utf-8'))
                raise HTTPException(status_code=response.status_code,
                                detail=f"could not store file: {response.content.decode('utf-8')}")
            assert response.json()["contentHash"] == content_hash.get_value()
            return content_hash
        except IOError as e:
            if e.errno == errno.EPIPE:
                raise HTTPException(status_code=500,
                                    detail=f"Could not send file to server!")
        ### Handle the error ###

    def metadata(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str]) -> httpx.Headers:
        self.__refresh_id_token()
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        headers = {} if not self.id_token else {"Authorization": f"Bearer {self.id_token}"}
        params = {
            "organization_id": organization_id,
            "content_hash": content_hash.get_value()
        }
        response = self.client.head(self.url, params=params, headers=headers)
        if response.status_code not in (200, 201):
            logging.warning(response.status_code, response.content.decode('utf-8'))
            raise HTTPException(status_code=response.status_code,
                                detail=f"could not get metadata from storage: {response.content.decode('utf-8')}")
        return response.headers

    def get_creation_contexts(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str]) -> List[str]:
        metadata = self.metadata(organization_id, content_hash)
        return [k.replace("-", "_") for k in metadata.keys() if str(k).startswith("creation-context")]

    def uri_for(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str]) -> str:
        return self.metadata(organization_id, content_hash)["url"]

    def update_metadata(self, organization_id: OrganizationId, content_hash: Union[FileContentHash, str], metadata: Dict[str, str]
                        ):
        self.__refresh_id_token()
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        headers = {} if not self.id_token else {"Authorization": f"Bearer {self.id_token}"}
        params = {
            "organization_id": organization_id,
            "content_hash": content_hash.get_value()
        }
        request = {
            "update": metadata
        }
        response = self.client.patch(self.url, params=params, headers=headers, json=request)
        if response.status_code not in (200, 201):
            logging.warning(response.status_code, response.content.decode('utf-8'))
            raise HTTPException(status_code=response.status_code,
                                detail=f"could not patch metadata: {response.content.decode('utf-8')}")
        return response.headers


storage = Storage()
