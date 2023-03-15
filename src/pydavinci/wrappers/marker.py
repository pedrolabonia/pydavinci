from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from typing_extensions import Literal, TypeAlias, TypedDict

import pydavinci.logger as log

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import (
        PyRemoteMediaPoolItem,
        PyRemoteTimeline,
        PyRemoteTimelineItem,
    )
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem
    from pydavinci.wrappers.timeline import Timeline
    from pydavinci.wrappers.timelineitem import TimelineItem

    PydavinciParent: TypeAlias = Union[TimelineItem, Timeline, MediaPoolItem]

    RemoteMarkerParent: TypeAlias = Union[
        PyRemoteMediaPoolItem, PyRemoteTimeline, PyRemoteTimelineItem
    ]


class _RemoteMarkerData(TypedDict):
    name: str
    color: str
    note: str
    duration: int
    customData: str


RemoteMarkerData: TypeAlias = Dict[int, "_RemoteMarkerData"]


class MarkerData(TypedDict):
    frameid: int
    name: str
    color: str
    note: str
    duration: int
    customdata: str


ATTRS = Literal["frameid", "customdata", "color", "name", "duration", "note"]

COLORS = Literal[
    "Blue",
    "Cyan",
    "Green",
    "Yellow",
    "Red",
    "Pink",
    "Purple",
    "Fuchsia",
    "Rose",
    "Lavender",
    "Sky",
    "Mint",
    "Lemon",
    "Sand",
    "Cocoa",
    "Cream",
]


class MarkerCollection:
    def __init__(self, obj: "PydavinciParent") -> None:
        self._obj: "PydavinciParent" = obj
        self._parent_obj: "RemoteMarkerParent" = obj._obj
        self._cache: Dict[int, Marker] = {}
        self.fetch()

    def add(
        self,
        frameid: int,
        color: COLORS,
        name: str,
        *,
        note: str = "",
        duration: int = 1,
        customdata: str = "",
        overwrite: bool = False,
    ) -> "Marker":
        """
        Adds a marker.

        ``customdata`` is a ``str`` that can be used for programatically
        setting and searching for markers. It's not exposed to the GUI.

        Args:
            frameid (int): frame for marker to be inserted at
            color (str): marker color
            name (str): marker name
            note (str, optional): marker note. Defaults to empty.
            duration (int, optional): marker duration. Defaults to 1 frame.
            customdata (str, optional): custom user data. Defaults to empty.
            overwrite (bool, optional): set to `True` if you want to overwrite an existing marker at that frameid.

        Returns:
            bool: `Marker` if successful
        """
        # return self._parent_obj.AddMarker(frameid, color, name, note, duration, customdata)

        if frameid in self._cache:
            if not overwrite:
                log.info(
                    f"Marker at {frameid} already exists. Skipping... If you want to overwrite, use overwrite = True"
                )
                return None  # type: ignore
            else:
                log.warn(f"Marker at frame {frameid} already exists. Overwriting ...")
                f = frameid
                self.delete(frameid=f)

        if self._parent_obj.AddMarker(frameid, color, name, note, duration, customdata):

            data: "MarkerData" = {
                "frameid": frameid,
                "color": color,
                "duration": duration,
                "note": note,
                "name": name,
                "customdata": customdata,
            }
            marker = Marker(self, self._parent_obj, data, frameid)
            self._cache_add(marker)
            return marker
        else:
            # TODO: try to inform user which error happened,
            # check if frameid and duration are OK for this clip
            log.error(
                "Couldn't add marker. Make sure the frameid is correct and the duration isn't bigger than the clips' length."
            )
            return None  # type: ignore

    def find(self, needle: str) -> Optional["Marker"]:
        """Finds the first marker that matches `needle` for the `Marker's` `note`, `name`, `customdata` or `color`.

        Returns:
            (Marker): first marker found with matching query
        """

        for marker in self._cache.values():
            if (
                needle == marker.note
                or needle == marker.name
                or needle == marker.customdata
                or needle == marker.color
            ):
                return marker

        return None

    def find_all(self, needle: str) -> Optional[List["Marker"]]:
        """Finds all markers that match `needle` for the `Marker's` `note`, `name`, `customdata` or `color`.

        Returns:
            (Optional[List[Marker]]): all markers found or if none found, returns `None`
        """
        _ret: List[Marker] = []

        for marker in self._cache.values():
            if (
                needle == marker.note
                or needle == marker.name
                or needle == marker.customdata
                or needle == marker.color
            ):
                _ret.append(marker)

        return _ret if _ret else None

    def get_custom(self, customdata: str) -> Dict[Any, Any]:
        """
        Gets custom marker by ``customdata``

        Args:
            customdata (str): custom data string

        Returns:
            dict: dict with marker data
        """
        return self._parent_obj.GetMarkerByCustomData(customdata)

    def delete(
        self,
        *,
        frameid: int = 0,
        color: COLORS = "",  # type: ignore
        customdata: str = "",
    ) -> bool:
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

        Deleting Markers:
            When selecting by ``frameid``, will delete single marker

            When selecting by ``color``, will delete _all_ markers with provided color

            When selecting by ``customdata``, will delete first marker with matching custom data
        """

        if frameid:
            del self._cache[frameid]
            return self._parent_obj.DeleteMarkerAtFrame(frameid)
        elif color:
            # Delete all entries in the cache that are not the specified color
            # DeleteMarkersByColor() deletes all with that specified color
            self._cache = {
                frame: marker for frame, marker in self._cache.items() if marker.color != color
            }
            return self._parent_obj.DeleteMarkersByColor(color)

        elif customdata:
            # DeleteMarkerByCustomData deletes the first frame entry with the specified customdata,
            # so we're grabbing the keys and sorting them to ensure we delete the right entry in our
            # cache

            sorted = list(self._cache.keys())
            sorted.sort()
            self._parent_obj.DeleteMarkerByCustomData(customdata)
            del self._cache[sorted[0]]
            return True

        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")

    def delete_all(self) -> None:
        """Deletes all markers"""
        for marker in self.all:
            marker.delete()

    @property
    def all(self) -> List["Marker"]:
        """Returns a list with all `Marker`'s

        Returns:
            (List[Marker])
        """
        self.fetch()
        return list(self._cache.values())

    def _cache_add(self, marker: "Marker") -> None:
        self._cache.update({marker._frameid: marker})

    def _cache_del(self, marker: "Marker") -> None:
        del self._cache[marker.frameid]

    def __iter__(self):  # type: ignore
        self.fetch()
        cache = self._cache.copy()
        yield from cache.values()

    def __repr__(self) -> str:
        markers = [str(x.frameid) for x in self.all]
        if len(markers) <= 4:
            displaystr = ", ".join(markers)
            return f"Markers(frames: {displaystr})"
        else:
            display: List[str] = markers[:2] + markers[-2:]
            display.insert(2, "...")
            displaystr = ", ".join(display)
            return f"Markers(Frames: {displaystr})"

    def fetch(self) -> None:
        """
        Fetch all markers from Davinci Resolve and updates `MarkerCollection`s internal cache. You probably won't need to use this.

        Why not:
            You would only use this if during the middle of the script execution a user manually added a marker. Otherwise, a `MarkerCollection` knows about all the markers
            it has deleted, added or updated, and `.fetch() ` is run on the class initialization.

        """
        markers: RemoteMarkerData = self._parent_obj.GetMarkers()
        if markers:
            for frameid in markers:
                marker: MarkerData = {
                    "frameid": frameid,
                    "color": markers[frameid]["color"],
                    "duration": markers[frameid]["duration"],
                    "name": markers[frameid]["name"],
                    "customdata": markers[frameid]["customData"],
                    "note": markers[frameid]["note"],
                }
                self._cache_add(Marker(self, self._parent_obj, marker, frameid))

        return


class Marker:
    def __init__(
        self,
        interface: "MarkerCollection",
        parent: "RemoteMarkerParent",
        data: "MarkerData",
        frameid: int,
    ) -> None:
        pass
        self._frameid = frameid
        self._data = data
        self._parent_obj = parent
        self._interface = interface

    def delete(self) -> None:
        """Deletes this `Marker`"""
        self._interface.delete(frameid=self._frameid)
        return

    @property
    def frameid(self) -> int:
        """Gets or changes this `Marker`'s `frameid`"""
        return self._data["frameid"]

    @frameid.setter
    def frameid(self, frameid: int) -> None:
        self.delete()
        self._frameid = frameid
        self._update("frameid", frameid)

    @property
    def customdata(self) -> str:
        """Gets or changes this `Marker`'s `customdata`"""
        return self._data["customdata"]

    @customdata.setter
    def customdata(self, customdata: str) -> None:
        if self._parent_obj.UpdateMarkerCustomData(self._frameid, customdata):
            self._data["customdata"] = customdata
            self._interface._cache_add(self)

    @property
    def name(self) -> str:
        """Gets or changes this `Marker`'s `name`"""
        return self._data["name"]

    @name.setter
    def name(self, name: str) -> None:
        self.delete()
        self._update("name", name)

    @property
    def color(self) -> str:
        """Gets or changes this `Marker`'s `color`"""
        return self._data["color"]

    @color.setter
    def color(self, color: Literal[COLORS]) -> None:
        # we don't have get_items on 3.6,
        # TODO update when support Davinci v18 and Python > 3.7
        if color not in COLORS.__values__:  # type: ignore
            return
        self.delete()
        self._update("color", color)

    @property
    def duration(self) -> int:
        """Gets or changes this `Marker`'s `duration`"""
        return self._data["duration"]

    @duration.setter
    def duration(self, duration: int) -> None:
        self.delete()
        self._update("duration", duration)

    @property
    def note(self) -> str:
        """Gets or changes this `Marker`'s `note`"""
        return self._data["note"]

    @note.setter
    def note(self, note: str) -> None:
        self.delete()
        self._update("note", note)

    def _update(self, key: ATTRS, value: Union[str, int]) -> None:
        self._data[key] = value  # type: ignore
        self._interface.add(
            frameid=self._data["frameid"],
            color=self._data["color"],  # type: ignore
            name=self._data["name"],
            note=self._data["note"],
            duration=self._data["duration"],
            customdata=self._data["customdata"],
        )
        return

    def __repr__(self) -> str:
        return f"Marker(Frame: {self.frameid}, custom: {self.customdata})'"
