from ..base import BaseModule


class DataQualityModule(BaseModule):
    """Simple data quality check that ensures input is not empty."""

    def run(self, data):
        if not data:
            raise ValueError("Received empty data")
        # Return data unchanged for this placeholder
        return data
