from glob import escape
from .getpath import GetPath
from .save import SaveFile

import os
import sys
from datetime import datetime

extpath = GetPath()

class QuickLog:
    def __init__(self, path: str = extpath.default(), debug: bool = False, override: bool = False, project: str = None) -> None:
        self.__debug = debug
        self.project = project
        if not self.__validate(path):
            sys.exit("ERROR: Path doesn't exists!")
        self.SAVE = SaveFile(path=self.path, override=override)


    def __validate(self, path) -> bool:
        if os.path.exists(path):
            __date = datetime.now()
            __date = __date.strftime("%m%d%Y")
            if self.project is None:
                self.path = f"{path}/{__date}.log"
            else:
                __project = self.project.lower()
                self.path = f"{path}/{__project}_{__date}.log"
            return True
        else:
            try:
                os.mkdir(path)
                if self.project is None:
                    self.path = f"{path}/{__date}.log"
                else:
                    __project = self.project.lower()
                    self.path = f"{path}/{__project}_{__date}.log"
                return True
            except Exception as err:
                print(err)
                return False


    def OK(self, text: str = None) -> None:
        __prefix = "[OK]"
        __date = datetime.now()
        __date = __date.strftime("%m/%d/%Y %H:%M:%S")
        if self.project is None:
            __text = f"{__date} - {__prefix}: {text}\n"
        else:
            __project = self.project.upper()
            __text = f"{__date} - {__project} - {__prefix}: {text}\n"
        text = f"🟢 {__prefix} {text}"
        if self.__debug:
            self.__DEBUG(text)


    def INFO(self, text: str = None, hidden: bool = False) -> None:
        __prefix = "[INFO]"
        __date = datetime.now()
        __date = __date.strftime("%m/%d/%Y %H:%M:%S")
        if self.project is None:
            __text = f"{__date} - {__prefix}: {text}\n"
        else:
            __project = self.project.upper()
            __text = f"{__date} - {__project} - {__prefix}: {text}\n"
        text = f"🔵 {__prefix} {text}"
        if self.__debug:
            self.__DEBUG(text)
        if not hidden:
            self.SAVE.save(__text)


    def WARNING(self, text: str = None, critical: bool = False, hidden: bool = False) -> None:
        __prefix = "[WARNING]"
        __date = datetime.now()
        __date = __date.strftime("%m/%d/%Y %H:%M:%S")
        if self.project is None:
            __text = f"{__date} - {__prefix}: {text}\n"
        else:
            __project = self.project.upper()
            __text = f"{__date} - {__project} - {__prefix}: {text}\n"
        text = f"🔴 {__prefix} {text}"
        if self.__debug:
            self.__DEBUG(text)
        else:
            if critical:
                self.__DEBUG(text)
                return False
        if not hidden:
            self.SAVE.save(__text)
            
    def API(self, text: str = None, status_code: int = 200) -> None:
        __prefix = "[API]"
        __date = datetime.now()
        __date = __date.strftime("%m/%d/%Y %H:%M:%S")
        if self.project is None:
            __text = f"{__date} - {__prefix}: {text}\n"
        else:
            __project = self.project.upper()
            __text = f"{__date} - {__project} - {__prefix}: {text}\n"
        if status_code == 200:
            text = f"🟢 {text}"
        elif not status_code == 200:
            text = f"🔴 {text}"
        else:
            text = f"⚪ {text}"
        if self.__debug:
            self.__DEBUG(text)
        self.SAVE.save(__text)

    def DEBUG(self, text: str = None, critical: bool = False, hidden: bool = False) -> None:
        __prefix = "[DEBUG]"
        __date = datetime.now()
        __date = __date.strftime("%m/%d/%Y %H:%M:%S")
        if self.project is None:
            __text = f"{__date} - {__prefix}: {text}\n"
        else:
            __project = self.project.upper()
            __text = f"{__date} - {__project} - {__prefix}: {text}\n"
        text = f"🟣 {__prefix} {text}"
        if self.__debug:
            self.__DEBUG(text)
        else:
            if critical:
                self.__DEBUG(text)
        if not hidden:
            self.SAVE.save(__text)


    def __DEBUG(self, display: str = None) -> None:
        print(display)


if __name__ == "__main__":
    log = Quicklog(project="Quicklog", path="logs", debug=False)
    log.INFO("Test")
    log.OK("Test")
    log.WARNING("Test", critical=True)
    log.DEBUG("Test", critical=True)