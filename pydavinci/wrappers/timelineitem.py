from typing import TYPE_CHECKING, Any, Dict, List

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteTimelineItem
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class TimelineItem(object):
    def __init__(self, *args: Any) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj: "PyRemoteTimelineItem" = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            raise TypeError(f"You need to provide at least one Resolve object.")

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

    def add_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.AddVersion(name, type)

    def delete_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.DeleteVersionByName(name, type)

    def load_color_version(self, name: str, type: int = 0) -> bool:
        return self._obj.LoadVersionByName(name, type)

    def rename_version(self, oldname: str, newname: str, type: int = 0) -> bool:
        return self._obj.RenameVersionByName(oldname, newname, type)

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
        Sets lut located on ``lut_path`` at ``node_index``

        Args:
            node_index (int): node index
            lut_path (str): lut path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetLUT(node_index, lut_path)

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
        return self._obj.GetSelectedTakeIndex()

    @take.setter
    def take(self, takeindex: int) -> bool:
        """
        Sets selected take

        Args:
            takeindex (int): take index for selection

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SelectTakeByIndex(takeindex)

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

    def __repr__(self) -> str:
        clip_repr = str(self.start) + "{| " + str(self.duration) + " |}" + str(self.end)
        return f'TimelineItem(Name:"{self.name}", In/Duration/Out: {clip_repr})'
