from ...base import BaseModule

class BaseReader(BaseModule):
    """Base class for all reader modules."""

    def run(self, data=None):
        raise NotImplementedError
