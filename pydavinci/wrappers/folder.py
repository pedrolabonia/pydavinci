# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class Folder(object):
    def __init__(self, obj) -> None:
        self._obj = obj

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
        return f'Folder(Name:"{self.name}"'
