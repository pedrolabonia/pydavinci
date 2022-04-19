from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pyremoteobject import PyRemoteObject

def get_resolveobjs(objs: List) -> List['PyRemoteObject']:
    return [x._obj for x in objs]


TRACK_TYPES = ["video", "audio", "subtitle"]
TRACK_ERROR = "Track type must be: 'video', 'audio', or 'subtitle"

