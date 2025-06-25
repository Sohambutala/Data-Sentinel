from .base import BaseWriter

class ConsoleWriter(BaseWriter):
    """Simple writer that prints the data."""

    def run(self, data):
        print(data)
        return data
