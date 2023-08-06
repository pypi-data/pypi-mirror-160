import os
import sys
import time

class SaveFile:
    def __init__(self, path: str, override: bool = False, debug: bool = False) -> None:
        self.path = path
        if override:
            self.mode = "w"
        else:
            self.mode = "a"
        self.debug = debug


    def save(self, text: str) -> None:
        try:
            __before = time.time()
            with open(self.path, self.mode) as file:
                file.write(text)
            __after = time.time()
            __time = format((__before - __after), ".4f")
            if self.debug:
                print(f"🕜 Saving the file took: {__time} seconds.")
        except Exception as err:
            sys.exit(err)