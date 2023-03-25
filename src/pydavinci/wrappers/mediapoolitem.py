from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.marker import MarkerCollection

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteMediaPoolItem


class MediaPoolItem:
    # TODO:
    # Implement a way to acess metadata such as mediapoolitem.metadata['Good Take'] = True
    # Meed to mess around with a private dict that uses
    # the SetMetadata() when internal dict updates

    def __init__(self, obj: "PyRemoteMediaPoolItem") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteMediaPoolItem" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

        self.markers = MarkerCollection(self)

    @property
    def name(self) -> str:
        """
        Returns:
            (str): ``MediaPoolItem`` name
        """
        return self._obj.GetName()

    def get_metadata(self, metadata_key: Optional[str] = None) -> Union[str, Dict[Any, Any]]:
        """Gets metadata ``metadata_key`` for ``MediaPoolItem``. If no ``metadata_key`` is provided,
           returns a ``Dict`` with all available metadata. Can return an empty ``dict`` if there's no metadata.

        Args:
            metadata_key (Optional[Any]): metadata key

        Returns:
            (Union[str, Dict[Any, Any]]): ``Dict`` or ``str`` corresponding to ``metadata_key``
        """
        if metadata_key:
            return self._obj.GetMetadata(metadata_key)
        return self._obj.GetMetadata()

    def set_metadata(self, meta_dict: Any) -> bool:
        """
        Sets metadata with ``meta_dict``:
        ```python
            meta_dict = {
                metadata_key: metadata value
                }
        ```

        It's recommended you validate which metadata you wan't to change first
        by using [MediaPoolItem.get_metadata()][pydavinci.wrappers.mediapoolitem.MediaPoolItem.get_metadata]
        and getting a dict with all the metadata to see which one you want to alter.

        This will probably change for the better for version 1.0

        Args:
            meta_dict (dict): dict with metadata to be set

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetMetadata(meta_dict)

    @property
    def media_id(self) -> str:
        """
        Returns:
            (str): ``MediaPoolItem`` UUID
        """
        return self._obj.GetMediaId()

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
            list of valid flag colors
        """
        return self._obj.GetFlagList()

    def clear_flags(self, color: str = "All") -> bool:
        """
        Clears flags

        Args:
            color (str, optional): Clears flag by ``color``. If none provided, defaults to "All" which clears all flags.

        Returns:
            ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearFlags(color)

    @property
    def color(self) -> str:
        """
        Gets or sets clip color

        Args:
            color (str): new clip color

        Returns:
            clip color
        """
        return self._obj.GetClipColor()

    @color.setter
    def color(self, color: str) -> bool:
        """
        Sets clip color

        Args:
            color (str): new clip color

        Returns:
            bool: _description_
        """
        return self._obj.SetClipColor(color)

    def clear_color(self) -> bool:
        """
        Clears clip color

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearClipColor()

    @property
    def properties(self) -> Union[str, Dict[Any, Any]]:
        """
        Gets all clip properties

        Returns:
            dict: dict with clip properties
        """
        return self._obj.GetClipProperty()

    def set_property(self, name: str, value: Union[str, int, float]) -> bool:
        """
        Sets property

        Args:
            name (str): property name
            value (Union[str, int, float]): property value

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetClipProperty(name, value)

    def link_proxy(self, path: str) -> bool:
        """
        Links media located at ``path`` to this ``MediaPoolItem``

        Args:
            path (str): _absolute_ path to proxy media

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LinkProxyMedia(path)

    def unlink_proxy(self) -> bool:
        """
        Unlinks proxy media of this ``MediaPoolItem``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UnlinkProxyMedia()

    def replace_clip(self, path: str) -> bool:
        """
        Replaces the underlying asset and metadata of ``MediaPoolItem`` with the specified absolute clip path.

        Args:
            path (str): path to clip

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ReplaceClip(path)

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `MediaPoolItem` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    def __repr__(self) -> str:
        return f'MediaPoolItem(Name:"{self.name})"'
