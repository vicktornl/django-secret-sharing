from datetime import timedelta
from typing import List, Tuple

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.utils import timezone

from django_secret_sharing import settings
from django_secret_sharing.backends.base import BaseBackend
from django_secret_sharing.exceptions import BackendError
from django_secret_sharing.models import File


class AWSBackend(BaseBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.get_client()
        self.bucket = self.get_bucket()

    def get_client(self):
        client_options = dict(
            endpoint_url=settings.AWS_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
            use_ssl=settings.AWS_USE_SSL,
            verify=settings.AWS_VERIFY,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        if settings.AWS_SIGNATURE_VERSION:
            client_options["config"] = Config(
                signature_version=settings.AWS_SIGNATURE_VERSION
            )
        return boto3.client("s3", **client_options)

    def get_bucket(self):
        return settings.AWS_BUCKET

    def validate_file_refs(self, file_refs: List[str]) -> bool:
        for file_ref in file_refs:
            # Prevent empty list items (often caused by bad javascript
            # implementations) causing to fail, skip them instead
            if file_ref == "":
                continue
            try:
                res = self.client.head_object(
                    Bucket=self.bucket,
                    Key=file_ref,
                )
                if not res.get("ResponseMetadata", None):
                    return False
            except ClientError as err:
                return False
        return True

    def delete_file(self, ref: str) -> bool:
        try:
            self.client.delete_object(
                Bucket=settings.AWS_BUCKET,
                Key=ref,
            )
        except ClientError:
            return False
        return True

    def delete_stale_files(
        self, expired_files: List[File], existing_file_refs: List[str]
    ) -> List[str]:
        deleted_file_refs = []

        for file in expired_files:
            if self.delete_file(file.ref):
                file.delete()
                deleted_file_refs.append(file.ref)

        res = self.client.list_objects(
            Bucket=settings.AWS_BUCKET,
            MaxKeys=1000,
        )

        if "Contents" not in res:
            return deleted_file_refs

        now = timezone.now()

        for obj in res["Contents"]:
            key = obj["Key"]

            if key not in existing_file_refs:
                last_modified = obj["LastModified"].astimezone(
                    timezone.get_current_timezone()
                )

                if last_modified <= now - timedelta(hours=1):
                    self.delete_file(key)
                    deleted_file_refs.append(key)

        return deleted_file_refs

    def get_upload_url(
        self, id: str, filename: str, expires_in: int = 3600
    ) -> Tuple[str, dict]:
        upload_path = self.get_upload_path(id, filename)
        try:
            res = self.client.generate_presigned_post(
                self.bucket,
                upload_path,
                Fields=None,
                Conditions=None,
                ExpiresIn=expires_in,
            )
        except ClientError as err:
            raise BackendError(str(err))
        url = res["url"]
        fields = res["fields"]
        return (url, fields)

    def get_download_url(self, file) -> str:
        try:
            res = self.client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket,
                    "Key": file.ref,
                },
                ExpiresIn=file.expires_in,
            )
        except ClientError as err:
            raise BackendError(str(err))
        return res
