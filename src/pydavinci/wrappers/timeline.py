from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pydavinci.logger as log
from pydavinci.exceptions import TimelineNotFound
from pydavinci.main import resolve_obj
from pydavinci.utils import TRACK_ERROR, TRACK_TYPES, get_resolveobjs, is_resolve_obj
from pydavinci.wrappers.marker import MarkerCollection
from pydavinci.wrappers.settings.constructor import get_tl_settings
from pydavinci.wrappers.timelineitem import TimelineItem


if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteTimeline
    from pydavinci.wrappers.gallerystill import GalleryStill
    from pydavinci.wrappers.settings.constructor import TimelineSettings


class Timeline:
    def __init__(self, *args: Any) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj: "PyRemoteTimeline" = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")

        else:
            _obj = resolve_obj.GetProjectManager().GetCurrentProject().GetCurrentTimeline()
            if _obj:
                self._obj = _obj
            else:
                raise TimelineNotFound(
                    extra="Couldn't find any active timeline. Are you sure there's any timeline in the project?"
                )

        self.markers = MarkerCollection(self)
        self._settings: Optional[TimelineSettings] = None

    def custom_settings(self, use: bool) -> bool:
        # Davinci only allows setting timeline settings if "useCustomSettings" is true, otherwise it returns False every time.
        """Allows this timeline to have settings independent from the project settings. See [Quickstart on Settings](../settings#project-vs-timeline-settings) for more details.

        Args:
            use (bool): ``True`` to use independent settings, ``False`` to follow project settings.

        """
        if use:
            return self.set_setting("useCustomSettings", "1")
        else:
            return self.set_setting("useCustomSettings", "0")

    @property
    def settings(self) -> "TimelineSettings":
        """Returns the [`TimelineSettings`](../settings/timeline) interface.
        [`Timeline.custom_settings(True)`](./#pydavinci.wrappers.timeline.Timeline.custom_settings) must be called first.
        """
        if self.get_setting("useCustomSettings") == "0":
            # doing the check here again in case user uses self.set_setting("useCustomSettings")
            # need to be compatible with that too

            log.error(
                "Can't create timeline settings. Timeline not configured for custom settings. "
                + "Use Timeline.custom_settings(True) and then call Timeline.settings again."  # noqa: W503
            )

            return  # type: ignore

        if self._settings:
            return self._settings
        else:
            self._settings = get_tl_settings(self)
            return self._settings

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

    def grab_all_stills(self, still_frame_source: int) -> List["GalleryStill"]:
        """
        Grabs stills from all the clips of the timeline.
        Args:
            still_frame_source: (1 - First frame, 2 - Middle frame)

        Returns:
            (List[GalleryStill]): list of ``GalleryStill`` objects
        """
        # TODO: Validate still_frame_source range
        return self._obj.GrabAllStills(still_frame_source)

    def grab_still(self) -> "GalleryStill":
        """
        Grabs still from the current video clip.
        Returns:
            GalleryStill: ``GalleryStill`` object
        """
        return self._obj.GrabStill()

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
        Gets current timecode (timecode at playhead)

        Returns:
            str: timecode
        """
        return self._obj.GetCurrentTimecode()

    @timecode.setter
    def timecode(self, timecode: str) -> bool:
        """
        Sets current timecode (moves playhead to timecode)

        Returns:
            str: timecode
        """
        return self._obj.SetCurrentTimecode(timecode)

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

    def export(
        self, file_name: str, export_type: str, export_subtype: Optional[str] = None
    ) -> bool:
        """
        Exports timeline file ``(.aaf, .xml, etc)``
        Supported ``export_type``:
        ```
        "AAF"
        "DRT"
        "EDL"
        "FCP_7_XML"
        "FCPXML_1_3"
        "FCPXML_1_4"
        "FCPXML_1_5"
        "FCPXML_1_6"
        "FCPXML_1_7"
        "FCPXML_1_8"
        "HDR_10_PROFILE_A"
        "HDR_10_PROFILE_B"
        "TEXT_CSV"
        "TEXT_TAB"
        "DOLBY_VISION_VER_2_9"
        "DOLBY_VISION_VER_4_0"
        ```

        Supported ``export_subtype``:
        ```python
        "NONE"
        "AAF_NEW"
        "AAF_EXISTING"
        "CDL"
        "SDL"
        "MISSING_CLIPS"
        ```

        Export types and subtypes:
            Please note that ``export_subtype`` is a required parameter for ``AAF`` and ``EDL``. For rest of the ``export_type``, ``export_subtype`` is ignored.

            When ``export_type`` is ``AAF``, valid ``export_subtype`` values are ``AAF_NEW`` and ``AAF_EXISTING``.

            When ``export_type`` is ``EXPORT_EDL``, valid export_dubtype values are ``EXPORT_CDL``, ``EXPORT_SDL``, ``EXPORT_MISSING_CLIPS`` and ``EXPORT_NONE``.

        Args:
            file_name (str): full filepath to export to including file name
            export_type (_type_): supported export type
            export_subtype (_type_): supported export subtype

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        export_type_map = {
            "AAF": 0.0,
            "DRT": 1.0,
            "EDL": 2.0,
            "FCP_7_XML": 3.0,
            "FCPXML_1_3": 4.0,
            "FCPXML_1_4": 5.0,
            "FCPXML_1_5": 6.0,
            "FCPXML_1_6": 7.0,
            "FCPXML_1_7": 8.0,
            "FCPXML_1_8": 9.0,
            "HDR_10_PROFILE_A": 10.0,
            "HDR_10_PROFILE_B": 11.0,
            "TEXT_CSV": 12.0,
            "TEXT_TAB": 13.0,
            "DOLBY_VISION_VER_2_9": 14.0,
            "DOLBY_VISION_VER_4_0": 15.0,
        }

        export_subtype_map = {
            "NONE": -1.0,
            "AAF_NEW": 0.0,
            "AAF_EXISTING": 1.0,
            "CDL": 2.0,
            "SDL": 3.0,
            "MISSING_CLIPS": 4.0,
        }

        if export_subtype:
            return self._obj.Export(
                file_name, export_type_map[export_type], export_subtype_map[export_subtype]
            )
        else:
            return self._obj.Export(file_name, export_type_map[export_type])

    def get_setting(
        self, settingname: Optional[str] = None
    ) -> Union[str, int, float, Dict[Any, Any]]:
        """
        _This function is a fallback if using [`Timeline.settings`][pydavinci.wrappers.timeline.Timeline.settings] doesn't work._

        Get timeline setting. If no setting provided, returns a dict with all settings.

        Args:
            settingname (str, optional): setting name.

        Returns:
            Union[str, Dict]: setting(s)
        """
        if settingname:
            return self._obj.GetSetting(settingname)
        return self._obj.GetSetting()

    def set_setting(self, setting_name: str, value: Union[str, int, float, Dict[Any, Any]]) -> bool:
        """
        _This function is a fallback if using [`Timeline.settings`][pydavinci.wrappers.timeline.Timeline.settings] doesn't work._

        Sets `Timeline` setting ``seting_name`` to ``value``

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

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `Timeline` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    def __repr__(self) -> str:
        return f"Timeline(name: {self.name})"
