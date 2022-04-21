import subprocess
import sys
import time
from typing import TYPE_CHECKING, List, Optional

import psutil
import pydavinci.main

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
}


def is_resolve_obj(obj):
    if type(obj) == type(pydavinci.main.resolve_obj):
        return obj
    else:
        return False


def get_proc_pid(name):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name"])
            if (
                pinfo["name"].lower() == name.lower()
                or pinfo["name"].lower() == f"{name.lower()}.exe"
            ):
                return pinfo["pid"]
        except psutil.AccessDenied:
            # System process
            pass
        except psutil.NoSuchProcess:
            # Process terminated
            pass
    return None


def process_active(process_name: str) -> bool:

    if process_name or f"{process_name}.exe" in (p.name().lower() for p in psutil.process_iter()):
        return True
    return False


def launch_resolve(headless: Optional[bool] = False, path: Optional[str] = None):

    if not get_proc_pid("resolve"):
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

        kwargs = {}
        print(args)
        # try:
        if system == "win":
            # Windows fuckery here to spawn a process without it being a child
            # of the python interpreter
            # https://docs.microsoft.com/pt-br/windows/win32/procthread/process-creation-flags?redirectedfrom=MSDN
            # this holds the tests...
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
        while not get_proc_pid("fuscript"):
            print("Waiting for fuscript")

        ready = False
        while not ready:
            time.sleep(0.3)
            print("...")
            try:
                print("try")
                if pydavinci.main.get_resolve().GetProjectManager() is not None:
                    print(pydavinci.main.get_resolve().GetProjectManager())
                    print("chego aqui")
                    ready = True
                    break
            except AttributeError:
                continue

        print("pronto pra vaza")
        time.sleep(4)
        return True

        # except FileNotFoundError:
        #     print("Davinci Resolve executable not found. Please double check the path")

    print("Davinci Resolve already running... Continuing")
