from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydavinci.main import resolve_obj
from pydavinci.utils import get_resolveobjs
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem
from pydavinci.wrappers.timeline import Timeline
from pydavinci.wrappers.timelineitem import TimelineItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteMediaPool


class MediaPool:
    def __init__(self) -> None:

        self._obj: PyRemoteMediaPool = (
            resolve_obj.GetProjectManager().GetCurrentProject().GetMediaPool()
        )

    @property
    def root_folder(self) -> "Folder":
        """
        Gets media pool root folder

        Returns:
            (Folder): media pool root folder
        """

        return Folder(self._obj.GetRootFolder())

    def add_subfolder(self, folder_name: str, parent_folder: "Folder") -> "Folder":
        """
        Adds subfolder ``folder_name`` into ``parent_folder``

        Args:
            folder_name (str): subfolder name
            parent_folder (Folder): parent folder object

        Returns:
            (Folder): created subfolder
        """
        return Folder(self._obj.AddSubFolder(parent_folder._obj, folder_name))

    def create_empty_timeline(self, timeline_name: str) -> "Timeline":
        """
        Creates empty timeline in current folder

        Args:
            timeline_name (str): timeline name

        Returns:
            (Timeline): created timeline
        """
        return Timeline(self._obj.CreateEmptyTimeline(timeline_name))

    def append_to_timeline(self, clips: List["MediaPoolItem"]) -> List["TimelineItem"]:
        """
        Appends a list of ``MediaPoolItem``s to current active timeline

        Args:
            clips (List[MediaPoolItem]): list of ``MediaPoolItem``s to append

        Returns:
            (List[TimelineItem]): list of inserted ``TimelineItem``s
        """
        # / TODO All types: MediaPoolItem, List[Dict], Dict
        appended = self._obj.AppendToTimeline(get_resolveobjs(clips))
        return [TimelineItem(x) for x in appended]

    def create_timeline_from_clips(self, name: str, clips: List["MediaPoolItem"]) -> "Timeline":
        """
        Creates timeline ``name`` from ``clips``

        Args:
            name (str): new timeline name
            clips (List[MediaPoolItem]): list of ``MediaPoolItem``s to use for creating the timeline

        Returns:
            (Timeline): created timeline
        """
        return Timeline(self._obj.CreateTimelineFromClips(name, get_resolveobjs(clips)))

    def import_timeline_fromfile(
        self, path: str, options: Optional[Dict[Any, Any]] = None
    ) -> "Timeline":
        """
        Imports a timeline from ``path`` with ``options``:

        ```python
            options = {
            "timelineName": str,
            # specifies the name of the timeline to be created

            "importSourceClips": bool,
            # specifies whether source clips should be imported, True by default

            "sourceClipsPath": str,
            # specifies a filesystem path to search for source clips if the media
            # is inaccessible in their original path and if "importSourceClips" is True

            "sourceClipsFolders": List[Folder]
            # to search for source clips if the media is not present in current folder
            # and if "importSourceClips" is False

            "interlaceProcessing": bool,
            # specifies whether to enable interlace processing on the imported
            # timeline being created. valid only for AAF import
            }
        ```
        Args:
            path (str): timeline file path
            options (dict, optional): Dict with import options. Defaults to `None`.

        Returns:
            (Timeline): created timeline
        """
        if not options:
            return Timeline(self._obj.ImportTimelineFromFile(path, options))
        return Timeline(self._obj.ImportTimelineFromFile(path))

    def delete_timelines(self, timelines: List["Timeline"]) -> bool:
        """
        Deletes timelines

        Args:
            timelines (List[Timeline]): list of timelines to be deleted

        Returns:
            bool: ``True`` if successful, ``False`` otherwise

        Info:
            If you want to delete only one timeline, you can wrap it in a single element list.
        """
        return self._obj.DeleteTimelines(get_resolveobjs(timelines))

    @property
    def current_folder(self) -> "Folder":
        """
        Gets current mediapool folder

        Returns:
            (Folder): current mediapool folder
        """
        return Folder(self._obj.GetCurrentFolder())

    def set_current_folder(self, folder: "Folder") -> bool:
        """
        Sets current mediapool folder

        Args:
            folder (Folder): desired ``Folder``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCurrentFolder(folder._obj)

    def delete_clips(self, clips: List["MediaPoolItem"]) -> bool:
        """
        Delete ``clips``

        Args:
            clips (List[MediaPoolItem]): list of ``MediaPoolItem``s to be deleted

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteClips(get_resolveobjs(clips))

    def delete_folders(self, folders: List["Folder"]) -> bool:
        """
        Delete ``folders``

        Args:
            folders (List[Folder]): list of ``Folder``s to be deleted

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteFolders(get_resolveobjs(folders))

    def move_clips(self, clips: List["MediaPoolItem"], folder: "Folder") -> bool:
        """
        Moves ``clips`` inside current active folder to ``folder``

        Args:
            clips (List[MediaPoolItem]): list of ``MediaPoolItem``s on current folder
            folder (Folder): destination folder

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.MoveClips(get_resolveobjs(clips), folder._obj)

    def move_folders(self, folders: List["Folder"], target_folder: "Folder") -> bool:
        """
        Move ``folders`` to ``target_folder``

        Args:
            folders (List[Folder]): List of folders to be moved. If you want to only use one folder, wrap it in a list.
            target_folder (Folder): target ``Folder``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.MoveFolders(get_resolveobjs(folders), target_folder._obj)

    def clip_mattes(self, clip: "MediaPoolItem") -> List[str]:
        """
        Gets paths of clip mattes from ``clip``

        Args:
            clip (MediaPoolItem): clip to get mattes from

        Returns:
            (List[str]): list of file paths associated with ``clip``'s mattes
        """
        return self._obj.GetClipMatteList(clip._obj)

    def timeline_mattes(self, folder: "Folder") -> List["MediaPoolItem"]:
        """
        Gets timeline mattes inside ``folder``

        Args:
            folder (Folder): folder to get timeline mattes from

        Returns:
            (List[MediaPoolItem]): list of timeline mattes
        """
        result = self._obj.GetTimelineMatteList(folder._obj)
        return [MediaPoolItem(x) for x in result]

    def delete_mattes_by_path(self, clip: "MediaPoolItem", path: List[str]) -> bool:
        """Delete mattes based on their file paths.

        Args:
            clip (MediaPoolItem): clip to have mattes deleted
            path (List[str]): list of matte paths

        Returns:
            bool: _description_
        """
        return self._obj.DeleteClipMattes(clip._obj, path)

    def relink_clips(self, clips: List["MediaPoolItem"], parent_folder: str) -> bool:
        """
        Update the folder location of specified media pool clips with the specified folder path.

        Args:
            clips (List[MediaPoolItem]): ``MediaPoolItem``s to relink
            parent_folder (str): new parent folder

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RelinkClips(get_resolveobjs(clips), parent_folder)

    def unlink_clips(self, clips: List["MediaPoolItem"]) -> bool:
        """
        Unlink ``clips``

        Args:
            clips (List[MediaPoolItem]): clips to be made offline

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UnlinkClips(get_resolveobjs(clips))

    def import_media(self, paths: List[str]) -> List["MediaPoolItem"]:
        """
        Import media from ``paths``

        Args:
            paths (List[str]): list of paths containing the media

        Returns:
            (List[MediaPoolItem]): list of imported ``MediaPoolItem``s

        Image Sequences:
            Doesn't support image sequences yet.
        """
        # / TODO: Implement image sequence using ImportMedia({ClipInfo})

        imported = self._obj.ImportMedia(paths)
        return [MediaPoolItem(x) for x in imported]

    def export_metadata(
        self, file_name: str, clips: Optional[List["MediaPoolItem"]] = None
    ) -> bool:
        """
        Exports metadata of specified clips to ``file_name.csv``.
            If no clips are specified, all clips from ``MediaPool`` will be used.

        Args:
            file_name (str): _description_
            clips (List[MediaPoolItem], optional): list of clips to be processed, defaults to ``None``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if clips:
            return self._obj.ExportMetadata(file_name, get_resolveobjs(clips))
        else:
            return self._obj.ExportMetadata(file_name)

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `MediaPool` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()
