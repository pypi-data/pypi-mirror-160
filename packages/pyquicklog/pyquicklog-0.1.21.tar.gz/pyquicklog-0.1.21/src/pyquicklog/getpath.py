import os
import sys

class GetPath:
    def __init__(self) -> None:
        self.system = os.name

    def default(self) -> str:
        if self.system == "nt":
            self.path = "C:\\Temp\\logs"
        else:
            self.path = "/tmp/logs"
        self.exists()
        return self.path

    def exists(self) -> None:
        if not os.path.exists(self.path):
            self.create()

    def create(self) -> None:
        try:
            os.mkdir(self.path)
        except Exception as err:
            sys.exit(err)