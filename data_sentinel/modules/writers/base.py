from ...base import BaseModule

class BaseWriter(BaseModule):
    """Base class for all writer modules."""

    def run(self, data):
        raise NotImplementedError
