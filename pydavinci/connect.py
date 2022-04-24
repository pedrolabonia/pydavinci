def load_fusionscript():  # type: ignore
    import imp
    import os
    import sys

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
                path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
            else:
                path = "/opt/resolve/libs/Fusion/"

            try:
                script_module = imp.load_dynamic(
                    "fusionscript", f"{path}fusionscript{ext}"
                )  # noqa: E501, B950 # type: ignore
            except ImportError:
                pass
