import importlib.util
import sys


def alternative_load_dynamic(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec) #type: ignore
    sys.modules[name] = module
    spec.loader.exec_module(module) # type: ignore
    return sys.modules[name]

def load_fusionscript():
    ext=".so"
    if sys.platform.startswith("darwin"):
        path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
    elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
        ext = ".dll"
        path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
    else:
        path = "/opt/resolve/libs/Fusion/"
    
    script_module = alternative_load_dynamic("fusionscript", path + "fusionscript" + ext)

    sys.modules[__name__] = script_module
    return
