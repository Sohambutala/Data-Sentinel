from .base import BaseReader

class S3Reader(BaseReader):
    """Example S3 reader (placeholder implementation)."""

    def run(self, data=None):
        bucket = self.config.get("bucket")
        key = self.config.get("key")
        return {"source": f"s3://{bucket}/{key}"}
