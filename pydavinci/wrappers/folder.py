from typing import TYPE_CHECKING, List

from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteFolder
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class Folder(object):
    def __init__(self, obj: "PyRemoteFolder") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteFolder" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def clips(self) -> List["MediaPoolItem"]:
        """
        Gets all clips

        Returns:
            List[MediaPoolItem]: list of clips
        """
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        objs = self._obj.GetClipList()
        return [MediaPoolItem(x) for x in objs]

    @property
    def name(self) -> str:
        """
        Gets folder name

        Returns:
            str: folder name
        """
        return self._obj.GetName()

    @property
    def subfolders(self) -> List["Folder"]:
        """
        Gets subfolders

        Returns:
            Dict: subfolders
        """
        return [Folder(x) for x in self._obj.GetSubFolderList()]

    def __repr__(self) -> str:
        return f'Folder(Name:"{self.name})"'
