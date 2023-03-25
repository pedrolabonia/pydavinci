from typing import TYPE_CHECKING, List


from pydavinci.utils import is_resolve_obj

from pydavinci.wrappers.gallerystillalbum import GalleryStillAlbum

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGallery


class Gallery:
    def __init__(self, obj: "PyRemoteGallery") -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteGallery" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    # TODO: Does "Album" adequately imply current album?
    # Not sure if I should follow "active_timeline" convention here.
    @property
    def album(self) -> "GalleryStillAlbum":
        """
        Returns current album as a ``GalleryStillAlbum`` object.

        Returns:
            GalleryStillAlbum: ``GalleryStillAlbum`` object
        """
        return GalleryStillAlbum(self._obj, self._obj.GetCurrentStillAlbum())

    @album.setter
    def album(self, gallery_still_album: str) -> bool:
        """
        Changes current album to ``GalleryStillAlbum`` object.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCurrentStillAlbum(gallery_still_album)

    @property
    def albums(self) -> List["GalleryStillAlbum"]:
        """
        List of ``GalleryStillAlbum`` objects.

        Returns:
            (List[GalleryStill]): List of ``GalleryStillAlbum`` objects
        """

        return [GalleryStillAlbum(self._obj, x) for x in self._obj.GetGalleryStillAlbums()]
