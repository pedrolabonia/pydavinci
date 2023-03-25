from typing import TYPE_CHECKING, Any, Dict, List, Union

from typing_extensions import Literal

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.marker import MarkerCollection
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteTimelineItem  # type: ignore


class TimelineItem:
    def __init__(self, obj: "PyRemoteTimelineItem") -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteTimelineItem" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

        self.markers = MarkerCollection(self)

    @property
    def name(self) -> str:
        """
        Gets name of ``TimelineItem``

        Returns:
            str: name
        """
        return self._obj.GetName()

    @property
    def duration(self) -> int:
        """
        Get duration in frames

        Returns:
            int: duration in frames
        """
        return self._obj.GetDuration()

    @property
    def start(self) -> int:
        """
        Returns the start frame position on the timeline.

        Returns:
            int: start frame position
        """
        return self._obj.GetStart()

    @property
    def end(self) -> int:
        """
        Returns the start frame position on the timeline.

        Returns:
            int: end frame position
        """
        return self._obj.GetEnd()

    @property
    def left_offset(self) -> int:
        """
        Returns the maximum extension by frame for clip from left side.

        Returns:
            int: left offset frame count
        """
        return self._obj.GetLeftOffset()

    @property
    def right_offset(self) -> int:
        """
        Returns the maximum extension by frame for clip from right side.

        Returns:
            int: right offset frame count
        """
        return self._obj.GetRightOffset()

    @property
    def properties(self) -> Dict[Any, Any]:
        """
        Gets all clip properties

        Returns:
            dict: dict with clip properties
        """

        return self._obj.GetProperty()

    def set_property(self, key: str, value: Union[str, int, float]) -> bool:
        """
        Sets property

        Args:
            name (str): property name
            value (Union[str, int, float]): property value

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """

        return self._obj.SetProperty(key, value)

    def add_flag(self, color: str) -> bool:
        """
        Adds flag

        Args:
            color (str): valid flag

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddFlag(color)

    @property
    def flags(self) -> List[str]:
        """
        Gets flag list

        Returns:
            List[str]: list of flags
        """
        return self._obj.GetFlagList()

    def clear_flags(self, color: str = "All") -> bool:
        """
        Clears all flags

        Args:
            color (str, optional): clears flags by ``color``. If `All` provided, clear all flags. Defaults to "All".

        Returns:
            bool: _description_
        """
        return self._obj.ClearFlags(color)

    @property
    def color(self) -> str:
        """
        Gets or sets clip color

        Args:
            color (str): color to be applied

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.GetClipColor()

    @color.setter
    def color(self, color: str) -> bool:
        """
        Sets clip color

        Args:
            color (str): color to be applied

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetClipColor(color)

    def clear_color(self) -> bool:
        """
        Clears clip color

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearClipColor()

        # TODO: Document these

    def add_color_version(self, name: str, type: Literal["local", "remote"]) -> bool:
        """Adds color version to this `TimelineItem`

        Args:
            name (str): version name
            type (Literal['local', 'remote']): whether to add a local or remote color version

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if type == "local":
            return self._obj.AddVersion(name, 0)
        elif type == "remote":
            return self._obj.AddVersion(name, 1)
        else:
            return False

    def delete_color_version(self, name: str, type: Literal["local", "remote"]) -> bool:
        """Adds color version from this `TimelineItem`

        Args:
            name (str): version name
            type (Literal['local', 'remote']): whether to delete a local or remote color version

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if type == "local":
            return self._obj.DeleteVersionByName(name, 0)
        elif type == "remote":
            return self._obj.DeleteVersionByName(name, 1)
        else:
            return False

    def load_color_version(self, name: str, type: Literal["local", "remote"]) -> bool:
        """Loads color version from `TimelineItem` named `name`

        Args:
            name (str): version name
            type (Literal['local', 'remote']): whether to load a local or remote color version

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if type == "local":
            return self._obj.LoadVersionByName(name, 0)
        elif type == "remote":
            return self._obj.LoadVersionByName(name, 1)
        else:
            return False

    def rename_version(self, oldname: str, newname: str, type: Literal["local", "remote"]) -> bool:
        """Renames a color version named `oldname` to `newname` on this `TimelineItem`

        Args:
            oldname (str): current version name
            newname (str): new version name
            type (Literal['local', 'remote']): whether to rename a local or remote color version

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if type == "local":
            return self._obj.RenameVersionByName(oldname, newname, 0)
        elif type == "remote":
            return self._obj.RenameVersionByName(oldname, newname, 1)
        else:
            return False

    @property
    def mediapoolitem(self) -> "MediaPoolItem":
        """
        Returns the corresponding ``MediaPoolItem`` for this ``TimelineItem``

        Returns:
            MediaPoolItem: ``MediaPoolItem``
        """
        return MediaPoolItem(self._obj.GetMediaPoolItem())

    # /TODO: Add Stero and Fusion wrappers

    def set_lut(self, node_index: int, lut_path: str) -> bool:
        """
        Sets LUT located on ``lut_path`` at ``node_index``

        Args:
            node_index (int): node index
            lut_path (str): lut path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetLUT(node_index, lut_path)

    def get_lut(self, node_index: int) -> "str":
        """
        Gets LUT at ``node_index``

        Args:
            node_index (int): node index

        Returns:
            str: LUT name. Example: ``'Sony/SLog3SGamut3.CineToLC-709TypeA.cube'``
        """
        return self._obj.GetLUT(node_index)

    def set_cdl(self, cdl: Dict[Any, Any]) -> bool:
        """
        Sets CDL

        Args:
            cdl (dict): valid CDL dict

        Example:
            ```python
            myclip.set_cdl({"NodeIndex" : "1",
            "Slope" : "0.5 0.4 0.2",
            "Offset" : "0.4 0.3 0.2",
            "Power" : "0.6 0.7 0.8",
            "Saturation" : "0.65"})
            ```

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCDL(cdl)

    def add_take(
        self, mediapool_item: "MediaPoolItem", startframe: int = 0, endframe: int = 0
    ) -> bool:
        """
        Adds ``mediapool_item`` as a new take. Initializes a take selector for the timeline item if needed.
        By default, the full clip extents is added. ``startframe`` and ``endFrame`` are
        optional arguments used to specify the extents.

        Args:
            mediapool_item (MediaPoolItem): media pool item to add as take
            startframe (int, optional): start frame for new take. Defaults to 0.
            endframe (int, optional): end frame for new take. Defaults to 0.

        Returns:
            bool: _description_
        """
        return self._obj.AddTake(mediapool_item._obj, startframe, endframe)

    @property
    def take(self) -> int:
        """
        Gets or sets current take

        Args:
            takeindex (int): take index for selection
        """
        return self._obj.GetSelectedTakeIndex()

    @take.setter
    def take(self, takeindex: int) -> None:
        """
        Sets selected take

        Args:
            takeindex (int): take index for selection

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        self._obj.SelectTakeByIndex(takeindex)

    @property
    def takes(self) -> int:
        """
        Get total number of takes

        Returns:
            int: total number of takes
        """
        return self._obj.GetTakesCount()

    def take_info(self, takeindex: int = 0) -> Dict[Any, Any]:
        """
        Gets take info. If no ``takeindex`` provided, uses current selected take.

        Args:
            takeindex (int, optional): take index to get info from. Defaults to current take.

        Returns:
            dict: _description_
        """
        if takeindex:
            return self._obj.GetTakeByIndex(takeindex)
        else:
            return self._obj.GetTakeByIndex(self._obj.GetSelectedTakeIndex())

    def delete_take(self, takeindex: int) -> bool:
        """
        Deletes take index with index ``takeindex``

        Args:
            takeindex (int): take index to be deleted

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteTakeByIndex(takeindex)

    def finalize_take(self, takeindex: int = 0) -> bool:
        """
        Finalizes take at ``takeindex``. If no ``takeindex`` provided, finalizes current take.

        Args:
            takeindex (int, optional): take index to be finalized. Defaults to current take.

        Returns:
            bool: _description_
        """
        if takeindex:
            self.take = takeindex
            return self._obj.FinalizeTake()
        else:
            return self._obj.FinalizeTake()

    def copy_grade_to(self, timeline_items: List["TimelineItem"]) -> bool:
        """
        Copies the current grade to all the items in ``timneline_items`` list

        Args:
            timeline_items (list): list with clips for the grade to be applied

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CopyGrades([x._obj for x in timeline_items])

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `TimelineItem` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    def __repr__(self) -> str:
        clip_repr = str(self.start) + "{| " + str(self.duration) + " |}" + str(self.end)
        return f'TimelineItem(Name:"{self.name}", In/Duration/Out: {clip_repr})'
