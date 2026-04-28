from contextlib import asynccontextmanager

from aiobotocore.session import get_session

from app_bot.config import s3_config


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.bucket_name = bucket_name
        self.session = get_session()

    @property
    def is_configured(self) -> bool:
        return all([self.access_key, self.secret_key, self.endpoint_url, self.bucket_name])

    @property
    def config(self) -> dict:
        return {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "endpoint_url": self.endpoint_url,
        }

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, name: str, file: bytes):
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=name, Body=file, ACL="public-read")
            endpoint_url = client.meta.endpoint_url.rstrip("/")
            return f"{endpoint_url}/{self.bucket_name}/{name}"


s3_client = S3Client(
    access_key=s3_config.ACCESS_KEY,
    secret_key=s3_config.SECRET_KEY,
    endpoint_url=s3_config.ENDPOINT_URL,
    bucket_name=s3_config.BUCKET_NAME,
)
