# type: ignore
# flake8: noqa
import imp
import os
import platform
import subprocess
import sys
import time
from collections.abc import MutableMapping
from typing import Dict, List, Optional

import psutil

from pydavinci.connect import load_fusionscript
from pydavinci.utils import default_resolve_install


class BaseResolveWrapper(object):
    def __init__(self, headless: Optional[bool] = None, path: Optional[str] = None) -> None:

        self.gui_latency = 7  # seconds

        self._obj = None
        # if davinci is not running, run it
        if not self.process_active("resolve"):
            self.launch_resolve(headless, path)
            print("vazei inner")

        self.load_fusionscript()

        import fusionscript as dvr_script

        self._obj = dvr_script.scriptapp("Resolve")
        # print(self._obj.GetProjectManager())

    @property
    def _root(self):
        import fusionscript as dvr_script

        return dvr_script.scriptapp("Resolve")

    # @staticmethod
    # def _get_project_manager(cls):
    #     return self._obj.GetProjectManager()

    # @staticmethod
    # def _get_media_storage(cls):
    #     return self._obj.GetMediaStorage()

    def load_fusionscript(self):

        WIN_ENV_VARIABLES = {
            "RESOLVE_SCRIPT_API": r"%PROGRAMDATA%\Blackmagic Design\DaVinciResolve\Support\Developer\Scripting",
            "RESOLVE_SCRIPT_LIB": r"C:\Program Files\Blackmagic Design\DaVinciResolve\fusionscript.dll",
            "PYTHONPATH": r"%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\\",
        }

        MAC_ENV_VARIABLES = {
            "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinciResolve/Developer/Scripting",
            "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinciResolve.app/Contents/Libraries/Fusion/fusionscript.so",
            "PYTHONPATH": "$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/",
        }
        LINUX_ENV_VARIABLES = {
            "RESOLVE_SCRIPT_API": "/opt/resolve/Developer/Scripting",
            "RESOLVE_SCRIPT_LIB": "/opt/resolve/libs/Fusion/fusionscript.so",
            "PYTHONPATH": "$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/",
        }

        if sys.platform.startswith("win32"):
            for key in WIN_ENV_VARIABLES.keys():
                os.environ[key] = WIN_ENV_VARIABLES[key]

        elif sys.platform.startswith("darwin"):
            for key in MAC_ENV_VARIABLES.keys():
                os.environ[key] = MAC_ENV_VARIABLES[key]

        else:
            for key in LINUX_ENV_VARIABLES.keys():
                os.environ[key] = LINUX_ENV_VARIABLES[key]

        script_module = None

        try:
            import fusionscript as script_module
        except ImportError:
            # Look for installer based environment variables:
            lib_path = os.getenv("RESOLVE_SCRIPT_LIB")
            if lib_path:
                try:
                    script_module = imp.load_dynamic("fusionscript", lib_path)
                except ImportError:
                    pass
            if not script_module:
                # Look for default install locations:
                ext = ".so"
                if sys.platform.startswith("darwin"):
                    path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
                elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
                    ext = ".dll"
                    path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
                elif sys.platform.startswith("linux"):
                    path = "/opt/resolve/libs/Fusion/"

                try:
                    script_module = imp.load_dynamic(
                        "fusionscript", path + "fusionscript" + ext
                    )  # noqa: E501, B950
                except ImportError:
                    pass

    def process_active(self, process_name: str) -> bool:

        if "wsl" in platform.uname().release.lower():
            # WSL, figure out a better place to do this error.
            raise SystemError("WSL not supported.")

        for p in psutil.process_iter():
            if (
                process_name.lower() in p.name().lower()
                or process_name.lower() + ".exe" in p.name().lower()
            ):
                print(f"Found process: {process_name}")
                return True
        return False

    def launch_resolve(self, headless: Optional[bool] = False, path: Optional[str] = None):

        if not self.process_active("resolve"):

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
                    # **kwargs,
                )
                print("subiu processo")
                while not self.process_active("fuscript"):
                    print("Waiting for fuscript")

                self.load_fusionscript()
                import fusionscript as dvr_script

                ready = False
                while not ready:
                    self._obj = dvr_script.scriptapp("Resolve")
                    try:
                        if dvr_script.scriptapp("Resolve") is not None:
                            ready = True
                    except AttributeError:
                        continue
                if not headless:
                    time.sleep(self.gui_latency)
                time.sleep(0.5)
                return

            except FileNotFoundError:
                print("Davinci Resolve executable not found. Please double check the path")

        print("Davinci Resolve already running... Continuing")
        return


class DavinciMarker(object):
    @property
    def markers(self) -> Dict:
        """Gets all markers

        Returns:
            Dict: dictionary with all markers

        Info:
            Markers comes formatted like so: `{frame: {data}}`
            ```python
                {157:
                {'color': 'Blue',
                'duration': 1,
                'note': '', # custom data
                'name': 'Marker 1',
                'customData': ''}}
            ```
        """

        return self._obj.GetMarkers()

    def add_marker(
        self,
        frameid: int,
        color: str,
        name: str,
        *,
        note: str = "",
        duration: int = 1,
        customdata: str = "",
    ) -> bool:
        """Adds marker

        Args:
            frameid (int): frame to insert marker
            color (str): marker color
            name (str): marker name
            note (str, optional): marker note
            duration (int, optional): marker duration.
            customdata (str, optional): marker custom data

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> Dict:
        """Returns a dict that's tagged with ``customdata``

        Args:
            customdata (str): custom data to search

        Returns:
            Dict: marker dictionary
        """
        return self._obj.GetMarkerByCustomData(customdata)

    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        """Updates custom marker at ``frameid`` with ``customdata``

        Args:
            frameid (int): frame id
            customdata (str): new custom data

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateMarkerCustomData(frameid, customdata)

    def get_marker_custom_data(self, frameid: int) -> str:
        """Gets marker custom data at ``frameid``

        Args:
            frameid (int): frame id

        Returns:
            str: custom data
        """
        return self._obj.GetMarkerCustomData(frameid)

    def delete_marker(self, *, frameid: int = 0, color: str = "", customdata: str = "") -> bool:
        """Deletes marker at ``frameid`` or with color ``color`` or with customdata ``customdata``.
        Pass one named parameter only.

        Args:
            frameid (int, optional): frame id
            color (str, optional): color
            customdata (str, optional): custom data

        Raises:
            ValueError: "You need to provide either ``frameid``, ``color`` or ``customdata``."

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color:
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")


class DavinciSettings(MutableMapping):
    def __init__(self, map):
        self.__data = map

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __setitem__(self, k, v):
        if k not in self.__data:
            raise KeyError(k)

        self.__data[k] = v

    def __delitem__(self, k):
        raise NotImplementedError

    def __getitem__(self, k):
        return self.__data[k]

    def __contains__(self, k):
        return k in self.__data
