import datetime
from typing import Tuple


class BaseBackend:
    def __init__(self, *args, **kwargs):
        pass

    def get_upload_path(self, id: str, filename: str) -> str:
        now = datetime.datetime.now()
        upload_path = f"uploads/{now.year}/{now.month}/{now.day}/{id}/{filename}"
        return upload_path

    def get_upload_url(self, filename: str, expires_in: int = 3600) -> Tuple[str, dict]:
        raise NotImplementedError(
            "subclasses of BaseBackend must provide a get_upload_url() method"
        )
