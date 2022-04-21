from pydavinci.connect import load_fusionscript
import functools


def get_resolve():
    load_fusionscript()
    import fusionscript as dvr_script  # type: ignore

    return dvr_script.scriptapp("Resolve")


resolve_obj = get_resolve()
