from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.main import resolve_obj
from pydavinci.utils import TRACK_ERROR, TRACK_TYPES, get_resolveobjs, is_resolve_obj
from pydavinci.wrappers.timelineitem import TimelineItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteTimeline


class Timeline(object):
    def __init__(self, *args: Any) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj: "PyRemoteTimeline" = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            self._obj = resolve_obj.GetProjectManager().GetCurrentProject().GetCurrentTimeline()

    @property
    def name(self) -> str:
        """
        Gets or sets timeline ``name``

        Args:
            name (str): new timeline name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> bool:
        """
        Changes timeline to ``name``

        Args:
            name (str): new timeline name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetName(name)

    def activate(self) -> bool:
        """
        Makes this timeline active

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return resolve_obj.GetProjectManager().GetCurrentProject().SetCurrentTimeline(self._obj)

    @property
    def start_frame(self) -> int:
        """
        Gets timeline start frame

        Returns:
            int: start frame
        """
        return self._obj.GetStartFrame()

    @property
    def end_frame(self) -> int:
        """
        Gets timeline end frame

        Returns:
            int: end frame
        """
        return self._obj.GetEndFrame()

    def track_count(self, track_type: str) -> int:
        """
        Gets track count on ``track_type``

        Args:
            track_type (str): valid ``track_types``: ``video``, ``audio``, ``subtitle``

        Raises:
            ValueError: Not a valid track type

        Returns:
            int: number of tracks
        """
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        else:
            return self._obj.GetTrackCount(track_type)

    def items(self, track_type: str, track_index: int) -> List["TimelineItem"]:
        """
        Gets [``TimelineItem``][pydavinci.wrappers.timelineitem.TimelineItem-attributes]s from a track

        Args:
            track_type (str): valid ``track_type``: ``video``, ``audio``, ``subtitle``
            track_index (int): track index. Starts at ``1``

        Raises:
            ValueError: Not a valid track type

        Returns:
            (List[TimelineItem]): list of items at specified track
        """
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)

        return [TimelineItem(x) for x in self._obj.GetItemListInTrack(track_type, track_index)]

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

        """
        return self._obj.UpdateMarkerCustomData(frameid, customdata)

    def get_marker_custom_data(self, frameid: int) -> str:
        """
        Gets marker ``customdata`` at ``frameid``

        Args:
            frameid (int): marker frame

        Returns:
            ``customdata``

        """
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

        Deleting Markers:
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

    def apply_grade_from_DRX(
        self, drx_path: str, grade_mode: int, timeline_items: List["TimelineItem"]
    ) -> bool:
        """
        Applies drx grade on a list of
        [``TimelineItem``][pydavinci.wrappers.timelineitem.TimelineItem-attributes]s

        Args:
            drx_path (str): path to a ``.drx`` file
            grade_mode (int): grade mode to use. ``0`` for ``No Keyframes``, ``1`` for ``Source Timecode aligned`` and ``2`` for ``Start Frames aligned``.
            timeline_items (List[TimelineItem]): timeline items to apply grade to

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ApplyGradeFromDRX(drx_path, grade_mode, [x._obj for x in timeline_items])

    @property
    def timecode(self) -> str:
        """
        Gets current timecode

        Returns:
            str: timecode
        """
        return self._obj.GetCurrentTimecode()

    @property
    def current_video_item(self) -> "TimelineItem":
        """
        Returns current video ``TimelineItem``

        Returns:
            TimelineItem: current ``TimelineItem``
        """
        if resolve_obj.GetCurrentPage() != "edit":
            raise Warning("You need to switch to edit page first before getting using this method.")
        return TimelineItem(self._obj.GetCurrentVideoItem())

    @property
    def current_clip_thumbnail(self) -> Dict[Any, Any]:
        """
        Returns a dict with data containing metadata + raw thumbnail
        image data (RGB 8-bit image data encoded in base64 format) for current media in the Color Page.

        Returns:
            dict: (keys "width", "height", "format" and "data")
        """
        return self._obj.GetCurrentClipThumbnailImage()

    def get_track_name(self, track_type: str, track_index: int) -> str:
        """
        Gets track name

        Args:
            track_type (str): valid track_type: ``video``, ``audio`` or ``subtitle``
            track_index (int): track index. Starts at ``1``

        Raises:
            ValueError: Not a valid track type

        Returns:
            str: track name
        """
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.GetTrackName(track_type, track_index)

    def set_track_name(self, track_type: str, track_index: int, new_name: str) -> bool:
        """
        Sets track name

        Args:
            track_type (str): valid track_type: ``video``, ``audio`` or ``subtitle``
            track_index (int): track index. Starts at ``1``
            new_name (str): new name

        Raises:
            ValueError: Not a valid track type

        Returns:
            (bool): ``True`` if successful, ``False`` otherwise
        """
        if track_type not in TRACK_TYPES:
            raise ValueError(TRACK_ERROR)
        return self._obj.SetTrackName(track_type, track_index, new_name)

    def duplicate_timeline(self, timeline_name: Optional[str] = None) -> "Timeline":
        """
        Duplicates this timeline

        Args:
            timeline_name (str, optional): New timeline name. If not provided, appends "Copy" to timeline name.

        Returns:
            (Timeline): new duplicated timeline
        """
        if timeline_name:
            return Timeline(self._obj.DuplicateTimeline(timeline_name))
        else:
            return Timeline(self._obj.DuplicateTimeline())

    def create_compound_clip(
        self, timeline_items: List["TimelineItem"], clip_info: Optional[Dict[Any, Any]] = None
    ) -> "TimelineItem":
        """
        Creates a compound clip using ``timeline_items``

        Args:
            timeline_items (List[TimelineItem]): list of ``TimelineItem``s to use
            clip_info (dict, optional): optional compound clip settings. Valid dict:
                ```python
                {"startTimecode" : "00:00:00:00", "name" : "Compound Clip 1"}
                ```

        Returns:
            (TimelineItem): compound clip
        """
        if not clip_info:
            return TimelineItem(self._obj.CreateCompoundClip(get_resolveobjs(timeline_items)))

        return TimelineItem(
            self._obj.CreateCompoundClip(get_resolveobjs(timeline_items), clip_info)
        )

    def create_fusion_clip(self, timeline_items: List["TimelineItem"]) -> "TimelineItem":
        """
        Creates a Fusion clip with ``timeline_items``

        Args:
            timeline_items (List[TimelineItem]): timeline items to be used as input in the Fusion clip

        Returns:
            (TimelineItem): resulting fusion clip
        """
        return TimelineItem(self._obj.CreateFusionClip(get_resolveobjs(timeline_items)))

    def import_aaf_into_timeline(
        self, file_path: str, import_options: Optional[Dict[Any, Any]] = None
    ) -> bool:  # noqa: E501
        """
        Imports an aaf into the timeline

        Import Options:
            Imports timeline items from an AAF file and optional ``import_options`` dict into the timeline, with support for the keys:

            ``"autoImportSourceClipsIntoMediaPool"``: ``bool``, specifies if source clips should be imported into media pool, ``True`` by default

            ``"ignoreFileExtensionsWhenMatching"``: ``bool``, specifies if file extensions should be ignored when matching, ``False`` by default

            ``"linkToSourceCameraFiles"``: bool, specifies if link to source camera files should be enabled, False by default

            ``"useSizingInfo"``: ``bool``, specifies if sizing information should be used, ``False`` by default

            ``"importMultiChannelAudioTracksAsLinkedGroups"``: bool, specifies if multi-channel audio tracks should be imported as linked groups, ``False`` by default

            ``"insertAdditionalTracks"``: bool, specifies if additional tracks should be inserted, ``True`` by default

            ``"insertWithOffset"``: ``str``, specifies insert with offset value in timecode format - defaults to ``"00:00:00:00"``, applicable if "insertAdditionalTracks" is False

            ``"sourceClipsPath"``: ``str``, specifies a filesystem path to search for source clips if the media is inaccessible in their original path and if ``"ignoreFileExtensionsWhenMatching"`` is ``True``

            ``"sourceClipsFolders"``: ``str``, list of ``Folder`` objects to search for source clips if the media is not present in current folder

        Args:
             file_path (str): path to ``.aaf`` file
             import_options (dict, optional): optional import options. See description above. Defaults to {}.

        Returns:
             bool: ``True`` if successful, ``False`` otherwise

        """
        if not import_options:
            return self._obj.ImportIntoTimeline(file_path)
        return self._obj.ImportIntoTimeline(file_path, import_options)

    def export(self, file_name: str, export_type: str, export_subtype: str) -> bool:
        """
        Exports timeline file ``(.aaf, .xml, etc)``
        Supported ``export_type``:
        ```python
        resolve.EXPORT_AAF
        resolve.EXPORT_DRT
        resolve.EXPORT_EDL
        resolve.EXPORT_FCP_7_XML
        resolve.EXPORT_FCPXML_1_3
        resolve.EXPORT_FCPXML_1_4
        resolve.EXPORT_FCPXML_1_5
        resolve.EXPORT_FCPXML_1_6
        resolve.EXPORT_FCPXML_1_7
        resolve.EXPORT_FCPXML_1_8
        resolve.EXPORT_HDR_10_PROFILE_A
        resolve.EXPORT_HDR_10_PROFILE_B
        resolve.EXPORT_TEXT_CSV
        resolve.EXPORT_TEXT_TAB
        resolve.EXPORT_DOLBY_VISION_VER_2_9
        resolve.EXPORT_DOLBY_VISION_VER_4_0
        ```

        Supported ``export_subtype``:
        ```python
        resolve.EXPORT_NONE
        resolve.EXPORT_AAF_NEW
        resolve.EXPORT_AAF_EXISTING
        resolve.EXPORT_CDL
        resolve.EXPORT_SDL
        resolve.EXPORT_MISSING_CLIPS
        ```

        Export types and subtypes:
            Please note that ``export_subtype`` is a required parameter for ``resolve.EXPORT_AAF`` and ``resolve.EXPORT_EDL``. For rest of the ``export_type``, ``export_subtype`` is ignored.

            When ``exportType`` is ``resolve.EXPORT_AAF``, valid ``export_subtype`` values are ``resolve.EXPORT_AAF_NEW`` and ``resolve.EXPORT_AAF_EXISTING``.

            When ``exportType`` is ``resolve.EXPORT_EDL``, valid exportSubtype values are ``resolve.EXPORT_CDL``, ``resolve.EXPORT_SDL``, ``resolve.EXPORT_MISSING_CLIPS`` and ``resolve.EXPORT_NONE``.

            Note: Replace ``resolve.`` when using the constants above, if a different ``Resolve`` class instance name is used.

        Args:
            file_name (str): full filepath to export to including file name
            export_type (_type_): supported export type
            export_subtype (_type_): supported export subtype

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        # / TODO: Do the Enums here. For now we're just passing as-is.
        return self._obj.Export(file_name, export_type, export_subtype)

    def get_setting(self, settingname: Optional[str] = None) -> str:
        """
        Get timeline setting. If no setting provided, returns a dict with all settings.

        Args:
            settingname (str, optional): setting name.

        Returns:
            Union[str, Dict]: setting(s)
        """
        if settingname:
            return self._obj.GetSetting(settingname)
        return self._obj.GetSetting()

    def set_setting(self, setting_name: str, value: Union[str, int, Dict[Any, Any]]) -> bool:
        """
        Set setting

        Args:
            setting_name (str): setting name
            value (Union[str, int, Dict[Any, Any]): setting value

        Returns:
           ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetSetting(setting_name, value)

    def insert_generator(self, generator_name: str) -> "TimelineItem":
        """
        Inserts a generator in the timeline

        Args:
            generator_name (str): generator name to be inserted

        Returns:
            (TimelineItem): generator
        """
        return TimelineItem(self._obj.InsertGeneratorIntoTimeline(generator_name))

    def insert_fusion_generator(self, generator_name: str) -> "TimelineItem":
        """
        Inserts a fusion generator in the timeline

        Args:
            generator_name (str): fusion generator name

        Returns:
            (TimelineItem): fusion generator
        """
        return TimelineItem(self._obj.InsertFusionGeneratorIntoTimeline(generator_name))

    def insert_ofx_generator(self, generator_name: str) -> "TimelineItem":
        """
        Inserts an OFX generator in the timeline

        Args:
            generator_name (str): OFX generator name

        Returns:
            (TimelineItem): OFX generator
        """
        return TimelineItem(self._obj.InsertOFXGeneratorIntoTimeline(generator_name))

    def insert_title(self, title_name: str) -> "TimelineItem":
        """
        Inserts a title in the timeline

        Args:
            title_name (str): title name

        Returns:
            (TimelineItem): title
        """
        return TimelineItem(self._obj.InsertTitleIntoTimeline(title_name))

    def insert_fusion_title(self, title_name: str) -> "TimelineItem":
        """
        Inserts a fusion title in the timeline

        Args:
            title_name (str): fusion title name

        Returns:
            (TimelineItem): fusion title
        """
        return TimelineItem(self._obj.InsertFusionTitleIntoTimeline(title_name))
