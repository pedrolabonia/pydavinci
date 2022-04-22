from typing import TYPE_CHECKING, List

from pydavinci.main import resolve_obj
from pydavinci.utils import is_resolve_obj
from pydavinci.pyremoteobject import PyRemoteObject

if TYPE_CHECKING:
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class Folder(object):
    def __init__(self, *args) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            raise TypeError(f"You need to provide at least one Resolve object.")

    @property
    def clips(self) -> List["MediaPoolItem"]:
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        objs = self._obj.GetClipList()
        return [MediaPoolItem(x) for x in objs]

    @property
    def name(self) -> str:
        return self._obj.GetName()

    @property
    def subfolders(self) -> List:
        return self._obj.GetSubFolderList()

    def __repr__(self) -> str:
        return f'Folder(Name:"{self.name})"'
