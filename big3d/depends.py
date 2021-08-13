"""Api dependency injection helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from boto3.resources.base import ServiceResource
    from botocore.client import BaseClient
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.service_resource import Bucket, S3ServiceResource


class BotoResource:
    client: BaseClient
    resource: ServiceResource
    svc_prefix: str

    def __init__(self, resource: str):
        self.svc_prefix = "big3d-api-dev"
        self.client = boto3.client(resource)
        self.resource = boto3.resource(resource)

    def __call__(self, *args, **kwargs) -> BotoResource:
        return self


class S3Bucket(BotoResource):
    resource: S3ServiceResource
    client: S3Client
    _bucket_name: str
    bucket: Bucket

    def __init__(self, bucket_name: str):
        super().__init__("s3")
        self._bucket_name = f"{self.svc_prefix}-{bucket_name}"
        self.bucket = None

    def __call__(self) -> S3Bucket:
        if not self.bucket:
            self.bucket = self.resource.Bucket(self._bucket_name)
        return self


RendersBucket = S3Bucket("renders")
