from typing import TYPE_CHECKING

from pydavinci.connect import load_fusionscript

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteResolve


def get_resolve() -> "PyRemoteResolve":
    load_fusionscript()  # type: ignore
    import fusionscript as dvr_script  # type: ignore

    return dvr_script.scriptapp("Resolve")  # type: ignore


resolve_obj: "PyRemoteResolve" = get_resolve()
