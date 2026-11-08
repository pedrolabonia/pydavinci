from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydavinci.utils import as_list, get_resolveobjs, is_resolve_obj
from pydavinci.wrappers._mixins import EffectMixin, FusionCompMixin, GradeMixin

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import (
        CDL,
        ExportFrameOptions,
        PhotoAlbumItemProperties,
        PyRemotePhotoAlbumItem,
    )
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class PhotoAlbumItem(FusionCompMixin, EffectMixin, GradeMixin):
    """A photo of a [``PhotoAlbum``][pydavinci.wrappers.photoalbum.PhotoAlbum] (Photo page, Resolve 21)."""

    def __init__(self, obj: "PyRemotePhotoAlbumItem") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemotePhotoAlbumItem" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def name(self) -> str:
        """
        Gets or sets the item name

        Returns:
            str: name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> None:
        self._obj.SetName(name)

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `PhotoAlbumItem` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    @property
    def mediapoolitem(self) -> Optional["MediaPoolItem"]:
        """
        Returns the ``MediaPoolItem`` of this photo

        Returns:
            Optional[MediaPoolItem]: media pool item
        """
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        item = self._obj.GetMediaPoolItem()
        return MediaPoolItem(item) if item else None

    def add_flag(self, color: str) -> bool:
        """
        Adds a flag

        Args:
            color (str): flag color

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddFlag(color)

    @property
    def flags(self) -> List[str]:
        """
        Gets flag list

        Returns:
            List[str]: flag colors
        """
        return as_list(self._obj.GetFlagList())

    def clear_flags(self, color: str = "All") -> bool:
        """
        Clears flags

        Args:
            color (str, optional): Clears flag by ``color``. Defaults to "All", which clears all flags.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearFlags(color)

    @property
    def color(self) -> str:
        """
        Gets or sets the item color

        Returns:
            str: color, empty if none is set
        """
        return self._obj.GetClipColor()

    @color.setter
    def color(self, color: str) -> None:
        self._obj.SetClipColor(color)

    def clear_color(self) -> bool:
        """
        Clears the item color

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearClipColor()

    @property
    def rating(self) -> int:
        """
        Gets or sets the star rating

        Returns:
            int: number of stars
        """
        return self._obj.GetRatings()

    @rating.setter
    def rating(self, stars: int) -> None:
        self._obj.SetRatings(stars)

    def copy_grade_to(self, photos: List["PhotoAlbumItem"]) -> bool:
        """
        Copies the grade of this photo to ``photos`` (Resolve 21.1.2: on the Photo page only)

        Args:
            photos (List[PhotoAlbumItem]): target photos

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CopyGrades(get_resolveobjs(photos))

    @property
    def current_color_version(self) -> Dict[str, Any]:
        """
        Returns the current color version (keys ``versionName``, ``versionType``)

        Returns:
            dict: version info
        """
        return self._obj.GetCurrentVersion()

    @property
    def color_versions(self) -> List[str]:
        """
        Returns the names of all color versions

        Returns:
            List[str]: version names
        """
        return as_list(self._obj.GetVersionNameList())

    def add_color_version(self, name: str) -> bool:
        """
        Adds color version ``name``

        Args:
            name (str): version name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddVersion(name)

    def delete_color_version(self, name: str) -> bool:
        """
        Deletes color version ``name``

        Args:
            name (str): version name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteVersionByName(name)

    def load_color_version(self, name: str) -> bool:
        """
        Loads color version ``name`` as the active version

        Args:
            name (str): version name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadVersionByName(name)

    def rename_version(self, oldname: str, newname: str) -> bool:
        """
        Renames color version ``oldname`` to ``newname``

        Args:
            oldname (str): current version name
            newname (str): new version name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RenameVersionByName(oldname, newname)

    def set_cdl(self, cdl: "CDL") -> bool:
        """
        Sets CDL values on a node, see ``TimelineItem.set_cdl``

        Args:
            cdl (dict): CDL dict with keys ``NodeIndex``, ``Slope``, ``Offset``, ``Power``, ``Saturation``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCDL(cdl)

    def export_frame(self, options: Optional["ExportFrameOptions"] = None) -> Dict[str, Any]:
        """
        Exports this photo as a still image

        Args:
            options (dict, optional): ``outputType`` (``"file"`` or ``"encodedString"``), ``encodedImageFormat``,
                ``filePath``, ``maxDimension``. Defaults to a base64 encoded jpg.

        Returns:
            dict: ``success``, ``error`` and ``data`` (base64 image for ``"encodedString"``)
        """
        if options is None:
            return self._obj.ExportFrame()
        return self._obj.ExportFrame(options)

    @property
    def properties(self) -> "PhotoAlbumItemProperties":
        """
        Gets all photo properties (see ``PhotoAlbumItemProperties`` in ``_resolve_stubs.pyi``)

        Returns:
            dict: properties
        """
        return self._obj.GetProperties()

    def set_properties(self, properties: "PhotoAlbumItemProperties") -> bool:
        """
        Sets photo properties. All keys are validated first - either all are set or none.

        Args:
            properties (dict): properties to set

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetProperties(properties)

    def __repr__(self) -> str:
        return f'PhotoAlbumItem(Name: "{self.name}")'
