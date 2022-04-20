import subprocess
import sys
import time
from typing import TYPE_CHECKING, List, Optional

import psutil

if TYPE_CHECKING:
    from pyremoteobject import PyRemoteObject


def get_resolveobjs(objs: List) -> List["PyRemoteObject"]:
    return [x._obj for x in objs]


TRACK_TYPES = ["video", "audio", "subtitle"]
TRACK_ERROR = "Track type must be: 'video', 'audio', or 'subtitle"


default_resolve_install = {
    "win": "",
    "mac": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve",
    "linux": "",
}


def process_active(process_name: str) -> bool:

    if process_name in (p.name().lower() for p in psutil.process_iter()):
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
        else:
            system = "linux"

        if path:
            args.append(path)
        else:
            args.append(default_resolve_install[system])

        if headless:
            args.append("-nogui")

        try:
            if system == "win":
                subprocess.Popen(
                    args,
                    start_new_session=True,
                    close_fds=True,
                    creationflags=DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )  # noqa: F821 type: ignore
                # windows needs extra flags for the processes to be detached

            else:  # POSIX
                subprocess.Popen(args, start_new_session=True, close_fds=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # type: ignore

            time.sleep(0.5)

            while not process_active("fuscript"):
                time.sleep(0.1)

            return

        except FileNotFoundError:
            print("Davinci Resolve executable not found. Please double check the path")

        print("Davinci resolve already running... Continuing")
