from typing import TYPE_CHECKING, Any, Dict, List

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteTimelineItem
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class TimelineItem(object):
    def __init__(self, *args: "PyRemoteTimelineItem") -> None:
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
    def duration(self) -> int:
        return self._obj.GetDuration()

    @property
    def start(self) -> int:
        return self._obj.GetStart()

    @property
    def end(self) -> int:
        return self._obj.GetEnd()

    @property
    def left_offset(self) -> int:
        return self._obj.GetLeftOffset()

    @property
    def right_offset(self) -> int:
        return self._obj.GetRightOffset()

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

    def get_custom_marker(self, customdata: str) -> Dict[Any, Any]:
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
    def markers(self) -> Dict[Any, Any]:
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
    def color(self, color: str) -> bool:
        return self._obj.SetClipColor(color)

    def clear_color(self) -> bool:
        return self._obj.ClearClipColor()

    def add_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.AddVersion(name, type)

    def delete_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.DeleteVersionByName(name, type)

    def load_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.LoadVersionByName(name, type)

    def rename_version(self, oldname: str, newname: str, type: int = 0) -> bool:
        return self._obj.RenameVersionByName(oldname, newname, type)

    @property
    def mediapoolitem(self) -> "MediaPoolItem":
        return MediaPoolItem(self._obj.GetMediaPoolItem())

    # /TODO: Add Stero and Fusion wrappers

    def set_lut(self, node_index: int, lut_path: str) -> bool:
        return self._obj.SetLUT(node_index, lut_path)

    def set_cdl(self, cdl: Dict[Any, Any]) -> bool:
        return self._obj.SetCDL(cdl)

    def add_take(
        self, mediapool_item: "MediaPoolItem", startframe: int = 0, endframe: int = 0
    ) -> bool:
        return self._obj.AddTake(mediapool_item._obj, startframe, endframe)

    @property
    def take(self) -> int:
        return self._obj.GetSelectedTakeIndex()

    @take.setter
    def take(self, takeindex: int) -> bool:
        return self._obj.SelectTakeByIndex(takeindex)

    @property
    def takes(self) -> int:
        return self._obj.GetTakesCount()

    def take_info(self, takeindex: int = 0) -> Dict[Any, Any]:
        if takeindex:
            return self._obj.GetTakeByIndex(takeindex)
        else:
            return self._obj.GetTakeByIndex(self._obj.GetSelectedTakeIndex())

    def delete_take(self, takeindex: int) -> bool:
        return self._obj.DeleteTakeByIndex(takeindex)

    def finalize_take(self, takeindex: int = 0) -> bool:
        if takeindex:
            self.take = takeindex
            return self._obj.FinalizeTake()
        else:
            return self._obj.FinalizeTake()

    def copy_grade_to(self, timeline_items: List["TimelineItem"]) -> bool:
        return self._obj.CopyGrades([x._obj for x in timeline_items])

    def __repr__(self) -> str:
        clip_repr = str(self.start) + "{| " + str(self.duration) + " |}" + str(self.end)
        return f'TimelineItem(Name:"{self.name}", In/Duration/Out: {clip_repr})'
