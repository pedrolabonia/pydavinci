from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.main import resolve_obj
from pydavinci.utils import as_list
from pydavinci.wrappers import constants
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import CloneStatus, PyRemoteMediaStorage


class MediaStorage:
    def __init__(self) -> None:
        self._obj: "PyRemoteMediaStorage" = resolve_obj.GetMediaStorage()

    @property
    def mounted_volumes(self) -> List[Any]:
        """
        Gets list of OS mounted volumes

        Returns:
            list: list of volumes
        """
        return self._obj.GetMountedVolumeList()

    def get_subfolders(self, folder_path: str) -> List[str]:
        """
        Gets subfolders on ``folder_path``

        Args:
            folder_path (str): parent folder

        Returns:
            List[str]: list of subfolders
        """
        return self._obj.GetSubFolderList(folder_path)

    def get_file_list(self, folder_path: str) -> List[str]:
        """
        Gets list of file on ``folder_path``

        Args:
            folder_path (str): parent folder

        Returns:
            List[str]: list of files in ``parent_folder``
        """
        return self._obj.GetFileList(folder_path)

    def reveal_in_storage(self, path: str) -> bool:
        """
        Opens ``path`` in media storage

        Args:
            path (str): path

        Returns:
            None: None
        """
        return self._obj.RevealInStorage(path)

    def add_clip_mattes(
        self, mediapool_item: "MediaPoolItem", paths: List[str], stereo_eye: Optional[str] = None
    ) -> bool:
        """
        Adds clip mattes from ``path`` in ``mediapool_item``

        Args:
            mediapool_item (MediaPoolItem): a MediaPoolItem object
            paths (Union[List[str], str]): A list of path strings or a single path string
            stereo_eye (str, optional): ``"left"`` or ``"right"`` for stereo clips

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if stereo_eye is None:
            return self._obj.AddClipMattesToMediaPool(mediapool_item._obj, paths)
        return self._obj.AddClipMattesToMediaPool(mediapool_item._obj, paths, stereo_eye)

    def add_timelilne_mattes(self, paths: List[str]) -> List["MediaPoolItem"]:
        """
        Adds timeline mattes into media pool

        Args:
            paths (Union[List[str], str]): a list of path strings or a single path string to a timeline matte

        Returns:
            List[MediaPoolItem]: list of timeline mattes ``MediaPoolItem``s
        """
        return [MediaPoolItem(x) for x in self._obj.AddTimelineMattesToMediaPool(paths)]

    def addclips_to_mediapool(
        self, item: List[Union[str, Dict[str, Any]]]
    ) -> List["MediaPoolItem"]:
        """
        Adds clips to media pool

        Args:
            item (List[Union[str, dict]]): a list of media paths or folders to add to media pool, or of dicts
                ``{"media": path, "startFrame": int, "endFrame": int}`` to add a part of a clip

        Returns:
            List[MediaPoolItem]: list of added ``MediaPoolItem``s

        Info:
            Even if you only added one clip, the returned ``MediaPoolItem`` will be inside a list. Access it directly by slicing it with the ``0`` index.
        """
        # /TODO Weird bug. Even if doing return type Union[List[MediaPoolItem], MediaPoolItem],
        # it doesn't identify the case that a single instace of MediaPoolItem might be returned,
        # and so on the linter it can't access the properties like .name

        # Work around is have everything output as a list right now, user should
        # have to use [0] on the object returned if it's a single clip.

        # if type(item) == type([]) and len(item) > 1:
        #     objs_added = [MediaPoolItem(x) for x in self._obj.AddItemListToMediaPool(item)]
        #     return objs_added
        # elif type(item) == type([]) and len(item) == 1:
        #     return [MediaPoolItem(self._obj.AddItemListToMediaPool(item[0]))]
        # else:
        #     return [MediaPoolItem(self._obj.AddItemListToMediaPool(item)[0])]

        objs_added = [MediaPoolItem(x) for x in as_list(self._obj.AddItemListToMediaPool(item))]
        return objs_added

    def set_clone_tool_settings(
        self,
        preserve_folder_name: Optional[bool] = None,
        checksum_type: Optional[Union[str, float]] = None,
    ) -> bool:
        """
        Sets the options of the Clone Tool, used by ``start_clone_media`` (and the Clone Tool UI)

        Args:
            preserve_folder_name (bool, optional): keep the source folder name. Resolve's default is ``False``.
            checksum_type (Union[str, float], optional): ``"none"``, ``"filesize"``, ``"crc32"``, ``"md5"``
                (Resolve's default), ``"sha256"``, ``"sha512"``, ``"xxh_64"`` or a ``CLONE_CHECKSUM_TYPE_*`` constant

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        settings: Dict[str, Any] = {}
        if preserve_folder_name is not None:
            settings["PreserveFolderName"] = preserve_folder_name
        if checksum_type is not None:
            settings["ChecksumType"] = constants.lookup("CLONE_CHECKSUM_TYPE_", checksum_type)
        return self._obj.SetCloneToolSettings(settings)

    def start_clone_media(self, source_dir: str, target_dirs: Union[str, List[str]]) -> bool:
        """
        Starts cloning ``source_dir`` to ``target_dirs`` (Clone Tool) - poll ``clone_status``

        Args:
            source_dir (str): source folder, e.g. a camera card
            target_dirs (Union[str, List[str]]): one or more target folders

        Returns:
            bool: ``True`` if the clone job was started, ``False`` otherwise
        """
        return self._obj.StartCloneMedia(source_dir, target_dirs)

    def stop_clone_media(self) -> bool:
        """
        Stops the running clone job

        Returns:
            bool: ``True`` if successful, ``False`` if no clone job is running
        """
        return self._obj.StopCloneMedia()

    @property
    def clone_status(self) -> "CloneStatus":
        """
        Returns the status of the current or last clone job

        Returns:
            dict: ``JobStatus`` (``"Complete"``, ``"Cloning"``, ``"Cancelled"``, ``"Failed"``),
            ``CompletionPercentage``, ``Error``
        """
        return self._obj.GetCloneStatus()
