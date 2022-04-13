import imp
import os
import sys

script_module = None

WIN_ENV_VARIABLES = {
        'RESOLVE_SCRIPT_API': r'%PROGRAMDATA%\Blackmagic Design\DaVinciResolve\Support\Developer\Scripting', 
        'RESOLVE_SCRIPT_LIB': r'C:\Program Files\Blackmagic Design\DaVinciResolve\fusionscript.dll', 
        'PYTHONPATH': "%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\\" #type: ignore
        }

MAC_ENV_VARIABLES = {
    'RESOLVE_SCRIPT_API':"/Library/Application Support/Blackmagic Design/DaVinciResolve/Developer/Scripting",
    'RESOLVE_SCRIPT_LIB':"/Applications/DaVinci Resolve/DaVinciResolve.app/Contents/Libraries/Fusion/fusionscript.so",
    'PYTHONPATH':"$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
}


if sys.platform.startswith('win32'):
    for key in WIN_ENV_VARIABLES.keys():
            os.environ[key] = WIN_ENV_VARIABLES[key]

elif sys.platform.startswith('darwin'):
    for key in MAC_ENV_VARIABLES.keys():
            os.environ[key] = MAC_ENV_VARIABLES[key]    

else:
    print('Linux not supported yet. Quitting program.')
    sys.exit(1)

try:
    import fusionscript as script_module  # type: ignore
except ImportError:
    # Look for installer based environment variables:
    import os
    lib_path=os.getenv("RESOLVE_SCRIPT_LIB")
    if lib_path:
        try:
            script_module = imp.load_dynamic("fusionscript", lib_path)
        except ImportError:
            pass
    if not script_module:
        # Look for default install locations:
        ext=".so"
        if sys.platform.startswith("darwin"):
            path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            ext = ".dll"
            path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
        elif sys.platform.startswith("linux"):
            path = "/opt/resolve/libs/Fusion/"

        try:
            script_module = imp.load_dynamic("fusionscript", path + "fusionscript" + ext) #type: ignore
        except ImportError:
            pass

if script_module:
    sys.modules[__name__] = script_module
    
else:
    raise ImportError("Could not locate module dependencies")
