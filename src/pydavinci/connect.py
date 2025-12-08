import imp
import os
import sys
import platform
import configparser
from tkinter import simpledialog

CONFIG_FILE = 'config.ini'

def save_config(script_api, script_lib, davinci_folder):
    config = configparser.ConfigParser()
    config['Paths'] = {
        'script_api': script_api,
        'script_lib': script_lib,
        'davinci_folder': davinci_folder
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'Paths' in config:
        return config['Paths']['script_api'], config['Paths']['script_lib'], config['Paths']['davinci_folder']
    return None, None, None

def prompt_user_for_paths():
    script_api = simpledialog.askstring("Input",
                                        r"Enter Davinci Script Api Path (Default is: %PROGRAMDATA%\Blackmagic Design\DaVinciResolve\Support\Developer\Scripting): ")
    script_lib = simpledialog.askstring("Input",
                                        r"Enter Davinci Script Lib Path (Default is: C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll): ")
    davinci_folder = simpledialog.askstring("Input",
                                            r"Enter Davinci Path (Default is: C:\Program Files\Blackmagic Design\DaVinci Resolve\): ")
    save_config(script_api, script_lib, davinci_folder)
    return script_api, script_lib, davinci_folder

def load_fusionscript():  # type: ignore
    import os
    if platform.system() == "Windows":
        script_api, script_lib, davinci_folder = load_config()
        if not script_api or not script_lib or not davinci_folder:
            script_api, script_lib, davinci_folder = prompt_user_for_paths()

    WIN_ENV_VARIABLES = {
        "RESOLVE_SCRIPT_API": fr"{script_api}",
        "RESOLVE_SCRIPT_LIB": fr"{script_lib}",
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
        import fusionscript as script_module  # type: ignore
    except ImportError:
        # Look for installer based environment variables:
        import os

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
                path = (
                    "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
                )
            elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
                ext = ".dll"
                path = fr"{davinci_folder}"
            else:
                path = "/opt/resolve/libs/Fusion/"

            try:
                script_module = imp.load_dynamic(
                    "fusionscript", f"{path}fusionscript{ext}"
                )  # noqa: E501, B950 # type: ignore
            except ImportError:
                pass
