# noqa: all
from collections.abc import MutableMapping
from typing import Dict


class BaseDavinciWrapper(object):
    def __init__(self) -> None:
        pass


class DavinciMarker(object):
    @property
    def markers(self) -> Dict:
        """Gets all markers

        Returns:
            Dict: dictionary with all markers

        Info:
            Markers comes formatted like so: `{frame: {data}}`
            ```python
                {157:
                {'color': 'Blue',
                'duration': 1,
                'note': '', # custom data
                'name': 'Marker 1',
                'customData': ''}}
            ```
        """

        return self._obj.GetMarkers()  # type: ignore

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
        """Adds marker

        Args:
            frameid (int): frame to insert marker
            color (str): marker color
            name (str): marker name
            note (str, optional): marker note
            duration (int, optional): marker duration.
            customdata (str, optional): marker custom data

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AddMarker(frameid, color, name, note, duration, customdata)  # type: ignore

    def get_custom_marker(self, customdata: str) -> Dict:
        """Returns a dict that's tagged with ``customdata``

        Args:
            customdata (str): custom data to search

        Returns:
            Dict: marker dictionary
        """
        return self._obj.GetMarkerByCustomData(customdata)  # type: ignore

    def update_custom_marker(self, frameid: int, customdata: str) -> bool:
        """Updates custom marker at ``frameid`` with ``customdata``

        Args:
            frameid (int): frame id
            customdata (str): new custom data

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateMarkerCustomData(frameid, customdata)  # type: ignore

    def marker_custom_data(self, frameid: int) -> str:
        """Gets marker custom data at ``frameid``

        Args:
            frameid (int): frame id

        Returns:
            str: custom data
        """
        return self._obj.GetMarkerCustomData(frameid)  # type: ignore

    def delete_marker(self, *, frameid: int = 0, color: str = "", customdata: str = "") -> bool:
        """Deletes marker at ``frameid`` or with color ``color`` or with customdata ``customdata``.
        Pass one named parameter only.

        Args:
            frameid (int, optional): frame id
            color (str, optional): color
            customdata (str, optional): custom data

        Raises:
            ValueError: "You need to provide either ``frameid``, ``color`` or ``customdata``."

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if frameid:
            return self._obj.DeleteMarkerAtFrame(frameid)  # type: ignore
        if color:
            return self._obj.DeleteMarkersByColor(color)  # type: ignore
        if customdata:
            return self._obj.DeleteMarkerByCustomData(customdata)  # type: ignore
        raise ValueError("You need to provide either 'frameid', 'color' or 'customdata'")


class DavinciSettings(MutableMapping):
    def __init__(self, map):
        self.__data = map

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __setitem__(self, k, v):
        if k not in self.__data:
            raise KeyError(k)

        self.__data[k] = v

    def __delitem__(self, k):
        raise NotImplementedError

    def __getitem__(self, k):
        return self.__data[k]

    def __contains__(self, k):
        return k in self.__data
