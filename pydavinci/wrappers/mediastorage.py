# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List, Union
from pydavinci.main import resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class MediaStorage(object):
    def __init__(self) -> None:
        self._obj = resolve_obj.GetMediaStorage()

    @property
    def mounted_volumes(self):
        return self._obj.GetMountedVolumeList()

    def get_subfolders(self, folder_path: str) -> List[str]:
        return self._obj.GetSubFolderList(folder_path)

    def get_file_list(self, folder_path: str) -> List[str]:
        return self._obj.GetFileList(folder_path)

    def reveal_in_storage(self, path: str) -> None:
        return self._obj.RevealInStorage(path)

    def add_clip_mattes(
        self, mediapool_item: "MediaPoolItem", paths: Union[List[str], str], *args
    ) -> bool:
        return self._obj.AddClipMattesToMediaPool(mediapool_item._obj, paths, *args)

    def add_timelilne_mattes(self, paths: Union[List[str], str]) -> List["MediaPoolItem"]:
        return self._obj.AddTimelineMattesToMediaPool(paths)

    def addclips_to_mediapool(self, item: List[str]) -> List["MediaPoolItem"]:
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
