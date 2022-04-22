from typing import Dict, List
from pydavinci.main import resolve_obj
from pydavinci.utils import is_resolve_obj


class MediaPoolItem(object):
    # TODO:
    # Implement a way to acess metadata such as mediapoolitem.metadata['Good Take'] = True
    # Meed to mess around with a private dict that uses
    # the SetMetadata() when internal dict updates

    def __init__(self, *args) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            raise TypeError(f"You need to provide at least one Resolve object.")

    @property
    def name(self) -> str:
        return self._obj.GetName()

    @property
    def metadata(self) -> Dict:
        return self._obj.GetMetadata()

    def set_metadata(self, meta_dict) -> bool:
        return self._obj.SetMetadata(meta_dict)

    @property
    def mediaid(self) -> str:
        return self._obj.GetMediaId()

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
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> Dict:
        return self._obj.GetMarkerByCustomData(customdata)

    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        return self._obj.UpdateMarkerCustomData(frameid, customdata)

    def marker_custom_data(self, frameid: int) -> str:
        return self._obj.GetMarkerCustomData(frameid)

    def delete_marker(self, *, frameid: int = 0, color: str = "", customdata: str = "") -> bool:
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color:
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")

    @property
    def markers(self) -> Dict:
        return self._obj.GetMarkers()

    def add_flag(self, color: str) -> bool:
        return self._obj.AddFlag(color)

    @property
    def flags(self) -> List[str]:
        return self._obj.GetFlagList()

    def clear_flags(self, color: str = "All") -> bool:
        return self._obj.ClearFlags(color)

    @property
    def color(self) -> str:
        return self._obj.GetClipColor()

    @color.setter
    def color(self, color) -> bool:
        return self._obj.SetClipColor(color)

    def clear_color(self) -> bool:
        return self._obj.ClearClipColor()

    @property
    def properties(self) -> Dict:
        return self._obj.GetClipProperty()

    def set_property(self, name: str, value: str) -> bool:
        return self._obj.SetClipProperty(name, value)

    def link_proxy(self, path: str) -> bool:
        return self._obj.LinkProxyMedia(path)

    def unlink_proxy(self, path: str) -> bool:
        return self._obj.UnlinkProxyMedia(path)

    def replace_clip(self, path: str) -> bool:
        return self._obj.ReplaceClip(path)

    def __repr__(self) -> str:
        return f'MediaPoolItem(Name:"{self.name})"'
