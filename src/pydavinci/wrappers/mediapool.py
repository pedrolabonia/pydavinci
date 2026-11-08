from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.main import resolve_obj
from pydavinci.utils import as_list, get_resolveobj, get_resolveobjs
from pydavinci.wrappers import constants
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem
from pydavinci.wrappers.timeline import Timeline
from pydavinci.wrappers.timelineitem import TimelineItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import MulticamOptions, PyRemoteMediaPool
    from pydavinci.wrappers.photoalbum import PhotoAlbum
    from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem


def _clip_info(clip: Union["MediaPoolItem", Dict[str, Any]]) -> Dict[str, Any]:
    """Clip info dict for ``AppendToTimeline`` / ``CreateTimelineFromClips``, with the raw ``mediaPoolItem``."""
    if isinstance(clip, dict):
        info = dict(clip)
        info["mediaPoolItem"] = get_resolveobj(info.get("mediaPoolItem"))
        return info
    return {"mediaPoolItem": get_resolveobj(clip)}


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

        Info:
            Resolve makes the new subfolder the current folder (the target of ``import_media``), and it accepts a name
            that is already used - check ``parent_folder.subfolders`` first if the call has to be idempotent.
        """
        return Folder(self._obj.AddSubFolder(parent_folder._obj, folder_name))

    def create_empty_timeline(self, timeline_name: str, timecode: Optional[str] = None) -> "Timeline":
        """
        Creates empty timeline in current folder

        Args:
            timeline_name (str): timeline name, must be unique
            timecode (str, optional): start timecode, e.g. ``"10:00:00:00"``. Defaults to the project setting.

        Returns:
            (Timeline): created timeline
        """
        if timecode is None:
            return Timeline(self._obj.CreateEmptyTimeline(timeline_name))
        return Timeline(self._obj.CreateEmptyTimeline(timeline_name, timecode))

    def append_to_timeline(
        self, clips: List[Union["MediaPoolItem", Dict[str, Any]]]
    ) -> List["TimelineItem"]:
        """
        Appends ``MediaPoolItem``s or clip info dicts to the current timeline

        Clip info:
            A clip info dict places a part of a clip:
            ```python
            {
                "mediaPoolItem": MediaPoolItem,  # pydavinci or Resolve object
                "startFrame": float,  # source start frame (optional)
                "endFrame": float,  # source end frame (optional)
                "mediaType": int,  # 1 - video only, 2 - audio only (optional)
                "trackIndex": int,  # destination track (optional)
                "recordFrame": float,  # timeline position (optional)
            }
            ```
            ``MediaPoolItem``s and dicts can be mixed.

        Args:
            clips (List[Union[MediaPoolItem, dict]]): ``MediaPoolItem``s and/or clip info dicts

        Returns:
            (List[TimelineItem]): list of inserted ``TimelineItem``s
        """
        if any(isinstance(clip, dict) for clip in clips):
            appended = self._obj.AppendToTimeline([_clip_info(clip) for clip in clips])
        else:
            appended = self._obj.AppendToTimeline(get_resolveobjs(clips))
        return [TimelineItem(x) for x in as_list(appended)]

    def create_timeline_from_clips(
        self, name: str, clips: List[Union["MediaPoolItem", Dict[str, Any]]]
    ) -> "Timeline":
        """
        Creates timeline ``name`` from ``clips``

        Clip info:
            Instead of a ``MediaPoolItem`` a clip info dict can place a part of a clip:
            ```python
            {
                "mediaPoolItem": MediaPoolItem,  # pydavinci or Resolve object
                "startFrame": float,  # source start frame (optional)
                "endFrame": float,  # source end frame (optional)
                "recordFrame": float,  # timeline position (optional)
            }
            ```

        Args:
            name (str): new timeline name
            clips (List[Union[MediaPoolItem, dict]]): ``MediaPoolItem``s and/or clip info dicts

        Returns:
            (Timeline): created timeline

        Info:
            Resolve 21.1.2 places each ``MediaPoolItem`` only once: further entries of the same clip (e.g. a second
            range) are dropped silently. For several ranges of one clip use ``create_empty_timeline`` and
            ``append_to_timeline``, which places every entry.
        """
        if any(isinstance(clip, dict) for clip in clips):
            return Timeline(
                self._obj.CreateTimelineFromClips(name, [_clip_info(clip) for clip in clips])
            )
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
            return Timeline(self._obj.ImportTimelineFromFile(path))
        options = dict(options)
        if "sourceClipsFolders" in options:
            options["sourceClipsFolders"] = get_resolveobjs(options["sourceClipsFolders"])
        return Timeline(self._obj.ImportTimelineFromFile(path, options))

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

    def import_media(
        self, paths: Union[str, Dict[str, Any], List[Union[str, Dict[str, Any]]]]
    ) -> List["MediaPoolItem"]:
        """
        Imports files, folders and image sequences into the current media pool folder

        Image Sequences:
            Pass a clip info dict per image sequence:
            ```python
            {
                "FilePath": "C:/shots/sh010/sh010.%04d.exr",  # %0Nd frame pattern
                "StartIndex": 1001,  # first frame
                "EndIndex": 1100,  # last frame
            }
            ```
            Paths and clip info dicts can be mixed. A dict with only ``"FilePath"`` is imported as a plain path:
            Resolve 21.1.2 rejects the dict form for anything but image sequences.

        Args:
            paths (Union[str, dict, List[Union[str, dict]]]): file/folder paths and/or clip info dicts

        Returns:
            (List[MediaPoolItem]): list of imported ``MediaPoolItem``s

        Info:
            Resolve imports paths and image sequences in separate calls. If one entry of a call cannot be imported
            (e.g. a missing file), Resolve imports nothing of that call - compare the result with what you passed.
        """
        if isinstance(paths, (str, dict)):
            paths = [paths]

        plain_paths: List[str] = []
        clip_infos: List[Dict[str, Any]] = []
        for path in paths:
            if isinstance(path, dict):
                if set(path) == {"FilePath"}:
                    plain_paths.append(path["FilePath"])
                else:
                    clip_infos.append(path)
            else:
                plain_paths.append(path)

        imported: List[Any] = []
        if plain_paths:
            imported += as_list(self._obj.ImportMedia(plain_paths))
        if clip_infos:
            imported += as_list(self._obj.ImportMedia(clip_infos))
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

    def auto_sync_audio(
        self,
        clips: List["MediaPoolItem"],
        sync_mode: Optional[Union[str, float]] = None,
        channel_number: Optional[Union[int, str, float]] = None,
        retain_embedded_audio: Optional[bool] = None,
        retain_video_metadata: Optional[bool] = None,
    ) -> bool:
        """
        Syncs the audio of ``clips``: links audio clips to the video clips they match. ``clips`` must contain at least
        one video and one audio clip.

        Arguments left at ``None`` use Resolve's default.

        Args:
            clips (List[MediaPoolItem]): video and audio clips to sync
            sync_mode (Union[str, float], optional): ``"waveform"``, ``"timecode"`` (default), ``"in"``, ``"out"``,
                ``"marker"`` or an ``AUDIO_SYNC_*`` constant
            channel_number (Union[int, str, float], optional): for ``"waveform"``: channel ``1`` (default) up to the
                lowest channel count of the clips, ``"automatic"``, ``"mix"`` or an ``AUDIO_SYNC_CHANNEL_*`` constant
            retain_embedded_audio (bool, optional): keep the embedded audio of the video clips. Defaults to ``False``.
            retain_video_metadata (bool, optional): keep the video metadata. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise

        Example:
            ```python
            mediapool.auto_sync_audio(clips, sync_mode="waveform", channel_number="automatic",
                                      retain_embedded_audio=True)
            ```
        """
        settings: Dict[str, Any] = {}
        if sync_mode is not None:
            settings["syncMode"] = constants.lookup("AUDIO_SYNC_", sync_mode)
        if channel_number is not None:
            settings["channelNumber"] = constants.lookup("AUDIO_SYNC_CHANNEL_", channel_number)
        if retain_embedded_audio is not None:
            settings["retainEmbeddedAudio"] = retain_embedded_audio
        if retain_video_metadata is not None:
            settings["retainVideoMetadata"] = retain_video_metadata
        return self._obj.AutoSyncAudio(get_resolveobjs(clips), settings)

    @property
    def selected_clips(self) -> List["MediaPoolItem"]:
        """
        Returns the ``MediaPoolItem``s selected in the media pool

        Returns:
            List[MediaPoolItem]: selected clips, empty if none is selected
        """
        return [MediaPoolItem(x) for x in as_list(self._obj.GetSelectedClips())]

    def set_selected_clip(self, clip: "MediaPoolItem") -> bool:
        """
        Selects ``clip`` in the media pool

        Args:
            clip (MediaPoolItem): clip to select

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetSelectedClip(get_resolveobj(clip))

    def refresh_folders(self) -> bool:
        """
        Updates the folders in collaboration mode

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RefreshFolders()

    def import_folder_from_file(self, path: str, source_clips_path: Optional[str] = None) -> bool:
        """
        Imports a folder from a ``.drb`` file

        Args:
            path (str): path to the ``.drb`` file
            source_clips_path (str, optional): folder to search for the source clips

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if source_clips_path is None:
            return self._obj.ImportFolderFromFile(path)
        return self._obj.ImportFolderFromFile(path, source_clips_path)

    def create_stereo_clip(self, left: "MediaPoolItem", right: "MediaPoolItem") -> "MediaPoolItem":
        """
        Creates a stereoscopic 3D clip from ``left`` and ``right``, it replaces both in the media pool

        Args:
            left (MediaPoolItem): left eye clip
            right (MediaPoolItem): right eye clip

        Returns:
            MediaPoolItem: stereo clip
        """
        return MediaPoolItem(self._obj.CreateStereoClip(get_resolveobj(left), get_resolveobj(right)))

    def create_multicam_clip(
        self, clips: List["MediaPoolItem"], options: "MulticamOptions"
    ) -> List["MediaPoolItem"]:
        """
        Creates multicam clips from ``clips``

        Args:
            clips (List[MediaPoolItem]): angles
            options (dict): ``name``, ``startTimecode``, ``frameRate``, ``angleSyncMode`` (``MULTICAM_ANGLE_SYNC_*``),
                ``channelConfig``, ``multicamAudioMode`` (``MULTICAM_AUDIO_*``), ``angleNameMode``
                (``MULTICAM_ANGLE_NAME_*``), ``splitAtGaps``, ``useFullClipExtents``, ``createBinForSourceClips``,
                ``detectSameCameraClipsMode`` (``MULTICAM_DETECT_*``) - see ``MulticamOptions`` in ``_resolve_stubs.pyi``

        Returns:
            List[MediaPoolItem]: created multicam clips

        Info:
            With ``createBinForSourceClips`` (default ``True``) Resolve moves the source clips into a new bin
            "Original Clips" in the current folder.
        """
        return [
            MediaPoolItem(x)
            for x in as_list(self._obj.CreateMulticamClip(get_resolveobjs(clips), options))
        ]

    def create_empty_photo_album(self, name: str) -> Optional["PhotoAlbum"]:
        """
        Creates an empty photo album

        Args:
            name (str): photo album name

        Returns:
            Optional[PhotoAlbum]: created photo album, ``None`` if it failed
        """
        from pydavinci.wrappers.photoalbum import PhotoAlbum

        album = self._obj.CreateEmptyPhotoAlbum(name)
        return PhotoAlbum(album) if album else None

    def create_photo_album_from_photos(
        self, name: str, photos: List["MediaPoolItem"]
    ) -> Optional["PhotoAlbum"]:
        """
        Creates a photo album with the still image clips ``photos``

        Args:
            name (str): photo album name
            photos (List[MediaPoolItem]): still image clips

        Returns:
            Optional[PhotoAlbum]: created photo album, ``None`` if it failed
        """
        from pydavinci.wrappers.photoalbum import PhotoAlbum

        album = self._obj.CreatePhotoAlbumFromPhotos(name, get_resolveobjs(photos))
        return PhotoAlbum(album) if album else None

    def delete_photo_albums(self, photo_albums: List["PhotoAlbum"]) -> bool:
        """
        Deletes ``photo_albums``

        Args:
            photo_albums (List[PhotoAlbum]): photo albums to delete

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeletePhotoAlbums(get_resolveobjs(photo_albums))

    def add_to_photo_album(self, photos: List["MediaPoolItem"]) -> List["PhotoAlbumItem"]:
        """
        Adds the still image clips ``photos`` to the current photo album. Resolve 21.1.2 adds them only while the
        Photo page is open (``Resolve.page = "photo"``), elsewhere it returns an empty list.

        Args:
            photos (List[MediaPoolItem]): still image clips

        Returns:
            List[PhotoAlbumItem]: added photo album items
        """
        from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem

        return [
            PhotoAlbumItem(x) for x in as_list(self._obj.AddToPhotoAlbum(get_resolveobjs(photos)))
        ]
