from typing import Dict, List, Optional

from pydavinci.main import resolve_obj, get_resolve
from pydavinci.utils import get_resolveobjs
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem
from pydavinci.wrappers.timeline import Timeline
from pydavinci.wrappers.timelineitem import TimelineItem


class MediaPool(object):
    def __init__(self) -> None:

        self._obj = get_resolve().GetProjectManager().GetCurrentProject().GetMediaPool()

    @property
    def root_folder(self) -> "Folder":

        return Folder(self._obj.GetRootFolder())

    def add_subfolder(self, parent_folder: "Folder", folder_name: str) -> "Folder":
        return Folder(self._obj.AddSubFolder(parent_folder._obj, folder_name))

    def create_empty_timeline(self, name: str) -> "Timeline":
        return Timeline(self._obj.CreateEmptyTimeline(name))

    def append_to_timeline(self, clips: List["MediaPoolItem"]) -> List["TimelineItem"]:
        # / TODO All types: MediaPoolItem, List[Dict], Dict
        appended = self._obj.AppendToTimeline(get_resolveobjs(clips))
        return [TimelineItem(x) for x in appended]

    def create_timeline_fromclips(self, name: str, clips: List["MediaPoolItem"]) -> "Timeline":
        return Timeline(self._obj.CreateTimelineFromClips(name, get_resolveobjs(clips)))

    def import_timeline_fromfile(self, path: str, options: Optional[Dict] = None) -> "Timeline":
        if not options:
            return Timeline(self._obj.ImportTimelineFromFile(path, options))
        return Timeline(self._obj.ImportTimelineFromFile(path))

    def delete_timelines(self, timelines: List["Timeline"]) -> bool:
        return self._obj.DeleteTimelines(get_resolveobjs(timelines))

    @property
    def current_folder(self) -> "Folder":
        return Folder(self._obj.GetCurrentFolder())

    def set_current_folder(self, folder: "Folder") -> bool:
        return self._obj.SetCurrentFolder(folder._obj)

    def delete_clips(self, clips: List["MediaPoolItem"]) -> bool:
        return self._obj.DeleteClips(get_resolveobjs(clips))

    def delete_folders(self, folders: List["Folder"]) -> bool:
        return self._obj.DeleteFolders(get_resolveobjs(folders))

    def move_clips(self, clips: List["MediaPoolItem"], folder: "Folder") -> bool:
        return self._obj.MoveClips(get_resolveobjs(clips), folder._obj)

    def move_folders(self, folders: List["Folder"], target_folder: "Folder") -> bool:
        return self._obj.MoveFolders(get_resolveobjs(folders), target_folder._obj)

    def clip_mattes(self, clip: "MediaPoolItem") -> List[str]:
        return self._obj.GetClipMatteList(clip._obj)

    def timeline_mattes(self, folder: "Folder") -> List["MediaPoolItem"]:
        result = self._obj.GetTimelineMatteList(folder._obj)
        return [MediaPoolItem(x) for x in result]

    def delete_mattes_bypath(self, clip: "MediaPoolItem", path: List[str]) -> bool:
        return self._obj.DeleteClipMattes(clip._obj, path)

    def relink_clips(self, clips: List["MediaPoolItem"], parent_folder: str) -> bool:
        return self._obj.RelinkClips(get_resolveobjs(clips), parent_folder)

    def unlink_clips(self, clips: List["MediaPoolItem"]) -> bool:
        return self._obj.UnlinkClips(get_resolveobjs(clips))

    def import_media(self, paths: List[str]) -> List["MediaPoolItem"]:
        # / TODO: Implement image sequence using ImportMedia({ClipInfo})

        imported = self._obj.ImportMedia(paths)
        return [MediaPoolItem(x) for x in imported]

    def export_metadata(self, file_name: str, clips: List["MediaPoolItem"]) -> bool:
        return self._obj.ExportMetadata(file_name, get_resolveobjs(clips))
