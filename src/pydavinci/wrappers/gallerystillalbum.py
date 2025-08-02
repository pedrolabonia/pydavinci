from typing import TYPE_CHECKING, List
from pydavinci.utils import is_resolve_obj

from pydavinci.wrappers.gallerystill import GalleryStill

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGallery  # type: ignore
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStillAlbum  # type: ignore


class GalleryStillAlbum:
    def __init__(
        self,
        parent_obj: "PyRemoteGallery",
        obj: "PyRemoteGalleryStillAlbum",
    ) -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteGalleryStillAlbum" = obj
            self.parent_obj: "PyRemoteGallery" = parent_obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def stills(self) -> List["GalleryStill"]:
        """
        List of ``GalleryStill`` objects in the album

        Returns:
            (List[GalleryStill]): List of ``GalleryStill`` objects
        """

        return [GalleryStill(self._obj, x) for x in self._obj.GetStills()]

    @property
    def name(self) -> str:

        # TODO: Is this really wrong to do?
        # I feel like it makes more sense for the name to be a property of the album
        # than to return an album object back to the gallery object.
        # Also I haven't seen any other instances of importing the resolve obj at this level.
        # So feeling very cheeky.

        return self.parent_obj.GetAlbumName(self._obj)

    @name.setter
    def name(self, name: str) -> bool:

        return self.parent_obj.SetAlbumName(self._obj, name)

    def export_stills(
        self, gallery_stills: List["GalleryStill"], folder_path: str, file_prefix: str, format_: str
    ) -> bool:
        """
        Exports list of ``GalleryStill`` objects to directory with ``file_prefix`` using ``format_``

        Supported ``format``:
        ```
        "dpx"
        "cin"
        "tif"
        "jpg"
        "png"
        "ppm"
        "bmp"
        "xpm"
        ```

        Args:
            gallery_stills (List[&quot;GalleryStill&quot;]): List of GalleryStill objects
            folder_path (str): Export directory
            file_prefix (str): Prefix for export filename
            format (str): Export format type

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """

        remote_gallery_stills = [x._obj for x in gallery_stills]
        return self._obj.ExportStills(remote_gallery_stills, folder_path, file_prefix, format_)

    def delete_stills(self, gallery_stills: List["GalleryStill"]) -> bool:
        """
        Deletes specified list of ``GalleryStill`` objects '[galleryStill]'

        Args:
            gallery_stills (List[&quot;GalleryStill&quot;]): List of GalleryStill objects

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """

        remote_gallery_stills = [x._obj for x in gallery_stills]
        return self._obj.DeleteStills(remote_gallery_stills)

    # TODO: Add repr method
    # Should ideally return name, but that's a method of the parent object.
    # See gallery.py

    # def __repr__(self) -> str:
    #     return f"GalleryStillAlbum(name: {self.name})"
