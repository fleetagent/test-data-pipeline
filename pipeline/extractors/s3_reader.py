import json
import boto3


class S3Reader:
    def __init__(self, bucket: str):
        self.s3 = boto3.client("s3")
        self.bucket = bucket

    def read_jsonl(self, prefix: str):
        paginator = self.s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                response = self.s3.get_object(Bucket=self.bucket, Key=obj["Key"])
                for line in response["Body"].iter_lines():
                    yield json.loads(line)
