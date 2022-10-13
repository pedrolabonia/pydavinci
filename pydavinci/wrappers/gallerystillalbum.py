from typing import TYPE_CHECKING, List
from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.gallerystill import GalleryStill

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStillAlbum  # type: ignore
    
class GalleryStillAlbum(object):
    def __init__(self, obj: "PyRemoteGalleryStillAlbum") -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteGalleryStillAlbum" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def stills(self) -> List["GalleryStill"]:
        """
        List of ``GalleryStill`` objects in the album

        Returns:
            (List[GalleryStill]): List of ``GalleryStill`` objects
        """
        return self._obj.GetStills()
      
    def get_label(self, gallery_still: "GalleryStill") -> str:
        """
        Gets the label of a ``GalleryStill`` object

        Returns:
            str: ``GalleryStill`` label
        """
        return self._obj.GetLabel(gallery_still)
    
    def set_label(self, gallery_still: "GalleryStill", label: str) -> bool:
        """
        Sets the ``label`` of a ``GalleryStill`` object

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetLabel(gallery_still, label)
    
    def export_stills(self, gallery_stills: List["GalleryStill"], folder_path: str, file_prefix: str, format_: str) -> bool:
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
        
        return self._obj.ExportStills(gallery_stills, folder_path, file_prefix, format_)
        
    def delete_stills(self, gallery_stills: List["GalleryStill"]) -> bool:
        """
        Deletes specified list of ``GalleryStill`` objects '[galleryStill]'

        Args:
            gallery_stills (List[&quot;GalleryStill&quot;]): List of GalleryStill objects
            
        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        
        return self._obj.DeleteStills(gallery_stills)

    # TODO: Add repr method
    # Should ideally return name, but that's a method of the parent object.
    # See gallery.py --in03
    
    # def __repr__(self) -> str:
    #     return f"GalleryStillAlbum(name: {self.name})"