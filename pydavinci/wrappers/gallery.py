from typing import TYPE_CHECKING, Any, Dict, List, Union

from typing_extensions import Literal

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.gallerystillalbum import GalleryStillAlbum
from pydavinci.wrappers.timeline import Timeline

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGallery  # type: ignore
    
class Gallery(object):
    def __init__(self, obj: "PyRemoteGallery") -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteGallery" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    # TODO: make get/set_album_name properties of "GalleryStillAlbum" instead of "Gallery"
    # Not sure how to go about this. Seems unnatural having to pass the album back to the
    # parent object just to get and set the album name. --in03
    
    def get_album_name(self, gallery_still_album: "GalleryStillAlbum") -> str:
        """
        Gets name of ``GalleryStillAlbum``

        Returns:
            str: name
        """
        return self._obj.GetAlbumName(gallery_still_album)
    
    def set_album_name(self, gallery_still_album: "GalleryStillAlbum", name: str) -> bool:
        """
        Changes ``GalleryStillAlbum`` name to ``name``

        Args:
            name (str): new ``GalleryStillAlbum`` name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetAlbumName(gallery_still_album, name)

    @property
    def album(self) -> bool:
        """
        Returns current album as a ``GalleryStillAlbum`` object.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.GetCurrentStillAlbum()
 
    @album.setter  
    def album(self, gallery_still_album: "GalleryStillAlbum") -> bool:
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
        return self._obj.GetGalleryStillAlbums()
    
def __repr__(self) -> str:
    current_album = self._obj.GetCurrentStillAlbum()
    return f"Gallery(Current album name: {self._obj.GetAlbumName(current_album)})"