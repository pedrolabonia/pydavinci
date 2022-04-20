import platform
import subprocess
import sys
from typing import TYPE_CHECKING, List, Optional

import psutil

from pydavinci.main import get_resolve

if TYPE_CHECKING:
    from pyremoteobject import PyRemoteObject


def get_resolveobjs(objs: List) -> List["PyRemoteObject"]:
    return [x._obj for x in objs]


TRACK_TYPES = ["video", "audio", "subtitle"]
TRACK_ERROR = "Track type must be: 'video', 'audio', or 'subtitle"


default_resolve_install = {
    "win": r"C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe",
    "mac": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve",
    "linux": "",
    "wsl": r"/mnt/c/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe",
}


def process_active(process_name: str) -> bool:
    if "wsl" in platform.uname().release.lower():
        # WSL, figure out a better place to do this error.
        raise SystemError("WSL not supported.")

    for p in psutil.process_iter():
        if (
            process_name.lower() in p.name().lower()
            or process_name.lower() + ".exe" in p.name().lower()  # type: ignore
        ):
            print(f"Found process: {process_name}")
            return True
    return False


def launch_resolve(headless: Optional[bool] = False, path: Optional[str] = None):

    if not process_active("resolve"):

        system: str = ""
        args: List = []

        if sys.platform.startswith("win32"):
            system = "win"
        elif sys.platform.startswith("darwin"):
            system = "mac"
        elif sys.platform.startswith("linux"):
            system = "linux"
        else:
            raise Exception("Can't find correct platform.")

        if path:
            args.append(path)
        else:
            args.append(default_resolve_install[system])

        if headless:
            args.append("-nogui")

        kwargs = {}

        try:
            if system == "win":
                # Windows fuckery here to spawn a process without it being a child
                # of the python interpreter
                # https://docs.microsoft.com/pt-br/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
            elif system == "wsl":
                args.insert(0, "cmd.exe")
            else:
                kwargs.update(close_fds=True)

            subprocess.Popen(
                args,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                **kwargs,
            )
            print("subiu processo")
            while not process_active("fuscript"):
                while not get_resolve():
                    pass

        except FileNotFoundError:
            print("Davinci Resolve executable not found. Please double check the path")

        return True

    print("Davinci Resolve already running... Continuing")
    return False
