class BaseModule:
    """Base class for all pipeline modules."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def run(self, data):
        """Run the module's logic.

        Parameters
        ----------
        data : Any
            Data passed from the previous stage.
        Returns
        -------
        Any
            Data to be passed to the next stage.
        """
        raise NotImplementedError
