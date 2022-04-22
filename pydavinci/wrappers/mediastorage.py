from typing import TYPE_CHECKING, Any, List

from pydavinci.main import resolve_obj
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteMediaStorage


class MediaStorage(object):
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
        self, mediapool_item: "MediaPoolItem", paths: List[str], stereo_eye: str
    ) -> bool:
        """
        Adds clip mattes from ``path`` in ``mediapool_item``

        Args:
            mediapool_item (MediaPoolItem): a MediaPoolItem object
            paths (Union[List[str], str]): A list of path strings or a single path string

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
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

    def addclips_to_mediapool(self, item: List[str]) -> List["MediaPoolItem"]:
        """
        Adds clips to media pool

        Args:
            item (List[str]): a list of media paths or folders to add to media pool

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

        objs_added = [MediaPoolItem(x) for x in self._obj.AddItemListToMediaPool(item)]
        return objs_added
