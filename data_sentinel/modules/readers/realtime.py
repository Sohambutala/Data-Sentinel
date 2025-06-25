from .base import BaseReader

class RealTimeReader(BaseReader):
    """Example real-time reader returning static data."""

    def run(self, data=None):
        records = self.config.get("records", [1, 2, 3])
        return {"records": records}
