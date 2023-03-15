from typing import TYPE_CHECKING
from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStill  # type: ignore
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStillAlbum  # type: ignore



        if is_resolve_obj(obj):
            self._obj: "PyRemoteGalleryStill" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")