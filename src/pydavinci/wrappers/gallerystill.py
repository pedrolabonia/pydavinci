from typing import TYPE_CHECKING
from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStill  # type: ignore
    from pydavinci.wrappers._resolve_stubs import PyRemoteGalleryStillAlbum  # type: ignore


class GalleryStill:
    def __init__(
        self, parent_obj: "PyRemoteGalleryStillAlbum", obj: "PyRemoteGalleryStill"
    ) -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteGalleryStill" = obj
            self.parent_obj: "PyRemoteGalleryStillAlbum" = parent_obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def label(self) -> str:
        """
        Gets the label of a ``GalleryStill`` object

        Returns:
            str: ``GalleryStill`` label
        """
        return self.parent_obj.GetLabel(self._obj)

    @label.setter
    def label(self, label: str) -> bool:
        """
        Sets the ``label`` of a ``GalleryStill`` object

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self.parent_obj.SetLabel(self._obj, label)
