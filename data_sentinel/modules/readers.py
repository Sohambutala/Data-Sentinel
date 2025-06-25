from ..base import BaseModule


class RealTimeReader(BaseModule):
    """Example real-time reader returning static data."""

    def run(self, data=None):
        records = self.config.get("records", [1, 2, 3])
        return {"records": records}


class S3Reader(BaseModule):
    """Example S3 reader (placeholder implementation)."""

    def run(self, data=None):
        bucket = self.config.get("bucket")
        key = self.config.get("key")
        return {"source": f"s3://{bucket}/{key}"}
