from typing import TYPE_CHECKING, Dict, List, Optional

from pydavinci.utils import TRACK_ERROR, TRACK_TYPES, get_resolveobjs

if TYPE_CHECKING:
    from pydavinci.wrappers.project import Project
    from pydavinci.wrappers.timelineitem import TimelineItem


class Timeline(object):
    def __init__(self, data=None) -> None:
        if data:
            self._obj = data
        else:
            self._obj = Project._obj.GetCurrentTimeline()

    @property
    def name(self) -> str:
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> bool:
        return self._obj.SetName(name)

    def activate(self):
        return Project._obj.SetCurrentTimeline(self._obj)

    @property
    def start_frame(self) -> int:
        return self._obj.GetStartFrame()

    @property
    def end_frame(self) -> int:
        return self._obj.GetEndFrame()

    def track_count(self, track_type) -> int:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        else:
            return self._obj.GetTrackCount(track_type)

    def items(self, track_type: str, track_index: int) -> List["TimelineItem"]:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)

        return [TimelineItem(x) for x in self._obj.GetItemListInTrack(track_type, track_index)]

    ### MARKER STUFF # noqa: E266
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
    def markers(self) -> dict:
        return self._obj.GetMarkers()

    ### END MARKER STUFF # noqa: E266

    def apply_grade_from_DRX(
        self, drx_path: str, grade_mode: int, timeline_items: List["TimelineItem"]
    ) -> bool:
        if isinstance(timeline_items, List):
            items = get_resolveobjs(timeline_items)
            return self._obj.ApplyGradeFromDRX(drx_path, grade_mode, items)
        else:
            raise ValueError("Timeline Items must be a list of TimelineItems")

    @property
    def timecode(self) -> str:
        return self._obj.GetCurrentTimecode()

    @property
    def current_video_item(self) -> "TimelineItem":
        return TimelineItem(self._obj.GetCurrentVideoItem())

    @property
    def current_clip_thumbnail(self) -> Dict:
        return self._obj.GetCurrentClipThumbnailImage()

    def get_track_name(self, track_type: str, track_index: int) -> str:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.GetTrackName(track_type, track_index)

    def set_track_name(self, track_type: str, track_index: int, new_name: str) -> bool:
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.SetTrackName(track_type, track_index, new_name)

    def duplicate_timeline(self, track_name: str = ""):
        if track_name:
            return Timeline(self._obj.DuplicateTimeline(track_name))
        else:
            return Timeline(self._obj.DuplicateTimeline())

    def create_compound_clip(
        self, timeline_items: List["TimelineItem"], clip_info: Optional[Dict] = None
    ) -> "TimelineItem":
        if not clip_info:
            return TimelineItem(self._obj.CreateCompountClip(get_resolveobjs(timeline_items)))

        return TimelineItem(
            self._obj.CreateCompountClip(get_resolveobjs(timeline_items), clip_info)
        )

    def create_fusion_clip(self, timeline_items: List["TimelineItem"]) -> "TimelineItem":
        return TimelineItem(self._obj.CreateFusionClip(get_resolveobjs(timeline_items)))

    def import_aaf_into_timeline(
        self, file_path: str, import_options: Optional[Dict] = None
    ) -> bool:  # noqa: E501
        if not import_options:
            return self._obj.ImportIntoTimeline(file_path)
        return self._obj.ImportIntoTimeline(file_path, import_options)

    def export(self, file_name: str, export_type, export_subtype) -> bool:
        # / TODO: Do the Enums here. For now we're just passing as-is.
        return self._obj.Export(file_name, export_type, export_subtype)

    def get_setting(self, settingname: str = "") -> str:
        if settingname == "":
            return self._obj.GetSetting()
        return self._obj.GetSetting(settingname)

    def set_setting(self, setting_name: str, value: str) -> bool:
        return self._obj.SetSetting(setting_name, value)

    def insert_generator(self, generator_name: str) -> "TimelineItem":
        return TimelineItem(self._obj.InsertGeneratorIntoTimeline(generator_name))

    def insert_fusion_generator(self, generator_name: str) -> "TimelineItem":
        return TimelineItem(self._obj.InsertFusionGeneratorIntoTimeline(generator_name))

    def insert_ofx_generator(self, generator_name: str) -> "TimelineItem":
        return TimelineItem(self._obj.InsertOFXGeneratorIntoTimeline(generator_name))

    def insert_title(self, title_name: str) -> "TimelineItem":
        return TimelineItem(self._obj.InsertTitleIntoTimeline(title_name))

    def insert_fusion_title(self, title_name: str) -> "TimelineItem":
        return TimelineItem(self._obj.InsertFusionTitleIntoTimeline(title_name))
