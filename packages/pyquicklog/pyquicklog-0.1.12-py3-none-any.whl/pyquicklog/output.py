import os
import sys


def _logpath() -> str:
    if os.name == "nt":
        path = "C:\Temp\logs"
    else:
        path = "/tmp/logs"
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print(e)
    return path


class LogOutput():
    def __init__(self, path: str = _logpath) -> None:
        self.path = path
        print(path)

    def save(self, text: str = None) -> None:
        with open(self.path, "a") as file:
            file.write(text + "\n")