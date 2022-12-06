import datetime
from typing import List, Tuple

from django_secret_sharing.models import File


class BaseBackend:
    def __init__(self, *args, **kwargs):
        pass

    def validate_file_refs(self, file_refs: List[str]) -> bool:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a validate_file_refs() method"
        )

    def delete_file(self, ref: str) -> bool:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a delete_file() method"
        )

    def delete_stale_files(
        self, expired_files: List[File], existing_file_refs: List[str]
    ) -> List[str]:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a delete_stale_files() method"
        )

    def get_upload_path(self, id: str, filename: str) -> str:
        now = datetime.datetime.now()
        upload_path = f"uploads/{now.year}/{now.month}/{now.day}/{id}/{filename}"
        return upload_path

    def get_upload_url(self, filename: str, expires_in: int = 3600) -> Tuple[str, dict]:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a get_upload_url() method"
        )

    def get_download_url(self, ref: str) -> str:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a get_download_url() method"
        )
