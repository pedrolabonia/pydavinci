from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteMediaPoolItem  # type: ignore


class MediaPoolItem(object):
    # TODO:
    # Implement a way to acess metadata such as mediapoolitem.metadata['Good Take'] = True
    # Meed to mess around with a private dict that uses
    # the SetMetadata() when internal dict updates

    def __init__(self, *args: Any) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj: "PyRemoteMediaPoolItem" = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            raise TypeError(f"You need to provide at least one Resolve object.")

    @property
    def name(self) -> str:
        """
        Returns:
            str: name
        """
        return self._obj.GetName()

    def get_metadata(self, metadata_type: Optional[Any]) -> Union[str, Dict[Any, Any]]:
        return self._obj.GetMetadata(metadata_type)

    def set_metadata(self, meta_dict: Any) -> bool:
        """
        Sets metadata

        Args:
            dict (dict): dict with metadata to be set

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetMetadata(meta_dict)

    @property
    def mediaid(self) -> str:
        """
        Returns:
            str: media id
        """
        return self._obj.GetMediaId()

    def add_marker(
        self,
        frameid: int,
        color: str,
        name: str,
        *,
        note: str = "",
        duration: int = 1,
        customdata: str = "",
    ) -> bool:
        """
        Adds a marker

        Args:
            frameid (int): frame for marker to be inserted at
            color (str): marker color
            name (str): marker name
            note (str, optional): marker note. Defaults to empty.
            duration (int, optional): marker duration. Defaults to 1 frame.
            customdata (str, optional): custom user data. Defaults to empty.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)

    def get_custom_marker(self, customdata: str) -> Dict[Any, Any]:
        """
        Gets custom marker by ``customdata``

        Args:
            customdata (str): custom data string

        Returns:
            dict: dict with marker data
        """
        return self._obj.GetMarkerByCustomData(customdata)

    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        """
        Updates marker at ``frameid`` with new ``customdata``

        Args:
            frameid (int): marker frame
            customdata (str): new customdata

        Returns:
            bool: ``True`` if successful, ``False`` otherwise

        Info:
        A marker's ``custom data`` is not exposed via UI and is useful for a scripting developer to attach any user specific data to markers.
        """
        return self._obj.UpdateMarkerCustomData(frameid, customdata)

    def marker_custom_data(self, frameid: int) -> str:
        return self._obj.GetMarkerCustomData(frameid)

    def delete_marker(self, *, frameid: int = 0, color: str = "", customdata: str = "") -> bool:
        """
        Deletes marker using ``frameid``, ``color`` or ``customdata``

        Args:
            frameid (int, optional): frameid to use for choosing which markers to delete
            color (str, optional): color to use for choosing which markers to delete
            customdata (str, optional): custom data to use for choosing which markers to delete

        Raises:
            ValueError: no valid params provided

        Returns:
            bool: ``True`` if successful, ``False`` otherwise

        Info:
            When selecting by ``frameid``, will delete single marker
            When selecting by ``color``, will delete _all_ markers with provided color
            When selecting by ``customdata``, will delete first marker with matching custom data
        """
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)
        if color:
            return self._obj.DeleteMarkersByColor(color)
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")

    @property
    def markers(self) -> Dict[Any, Any]:
        """
        Gets markers

        Returns:
            dict: markers
        """
        return self._obj.GetMarkers()

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
            List[str]: list of valid flag colors
        """
        return self._obj.GetFlagList()

    def clear_flags(self, color: str = "All") -> bool:
        """
        Clears flags

        Args:
            color (str, optional): Clears flag by ``color``. If none provided, defaults to "All" which clears all flags.

        Returns:
            bool: _description_
        """
        return self._obj.ClearFlags(color)

    @property
    def color(self) -> str:
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

    def set_property(self, name: str, value: str) -> bool:
        """
        Sets property

        Args:
            name (str): property name
            value (str): property value

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

    def __repr__(self) -> str:
        return f'MediaPoolItem(Name:"{self.name})"'
