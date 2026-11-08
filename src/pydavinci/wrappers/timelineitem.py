import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from typing_extensions import Literal

from pydavinci.utils import as_list, get_resolveobjs, is_resolve_obj
from pydavinci.wrappers import constants
from pydavinci.wrappers._mixins import EffectMixin, FusionCompMixin, GradeMixin
from pydavinci.wrappers.marker import MarkerCollection
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import (  # type: ignore
        CopyAttributesOptions,
        ExportFrameOptions,
        FadeInfo,
        OutputBlanking,
        PyRemoteTimelineItem,
        RemoveSilenceOptions,
        SmartSwitchSettings,
        SpeedOptions,
        TimelineItemPosition,
        TimelineItemProperties,
        TransitionOptions,
        VoiceIsolationState,
    )


def _cache_mode(value: Union[bool, str, float]) -> Union[float, int]:
    """CACHE_* value for the render cache setters: Resolve 21.1.2 rejects bools and strings."""
    if isinstance(value, bool):
        return constants.CACHE_ENABLED if value else constants.CACHE_DISABLED
    if isinstance(value, str) and value.strip().lower() == "auto":
        return constants.CACHE_AUTO_ENABLED
    return constants.lookup("CACHE_", value)


class TimelineItem(FusionCompMixin, EffectMixin, GradeMixin):
    def __init__(self, obj: "PyRemoteTimelineItem") -> None:

        if is_resolve_obj(obj):
            self._obj: "PyRemoteTimelineItem" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

        self.markers = MarkerCollection(self)

    @property
    def name(self) -> str:
        """
        Gets or sets name of ``TimelineItem``.
        Use [``set_name``][pydavinci.wrappers.timelineitem.TimelineItem.set_name] to check the result.

        Returns:
            str: name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> None:
        self._obj.SetName(name)

    def set_name(self, name: str) -> bool:
        """
        Sets the item name

        Args:
            name (str): new name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetName(name)

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
        Gets all clip properties (see ``TimelineItemProperties`` in ``_resolve_stubs.pyi``)

        Returns:
            dict: dict with clip properties
        """
        # GetProperty() is deprecated since Resolve 20 - GetProperties() returns the same dict
        return self._obj.GetProperties()

    def set_property(self, key: str, value: Union[str, int, float]) -> bool:
        """
        Sets property

        Args:
            name (str): property name
            value (Union[str, int, float]): property value

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        # SetProperty(key, value) is deprecated since Resolve 20
        return self._obj.SetProperties({key: value})

    def set_properties(self, properties: "TimelineItemProperties") -> bool:
        """
        Sets several clip properties. All keys and values are validated first - either all are set or none.

        Args:
            properties (dict): property names and values, e.g. ``{"ZoomX": 1.2, "ZoomY": 1.2}``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetProperties(properties)

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

    @property
    def type(self) -> str:
        """
        Returns the item type

        Returns:
            str: ``"video"``, ``"audio"``, ``"generator"`` or ``"transition"``
        """
        return self._obj.GetType()

    @property
    def enabled(self) -> bool:
        """
        Gets or sets whether the clip is enabled

        Returns:
            bool: ``True`` if enabled
        """
        return self._obj.GetClipEnabled()

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._obj.SetClipEnabled(enabled)

    @property
    def source_start_frame(self) -> int:
        """
        Returns the start frame of the used part of the media pool clip

        Returns:
            int: source start frame
        """
        return self._obj.GetSourceStartFrame()

    @property
    def source_end_frame(self) -> int:
        """
        Returns the end frame of the used part of the media pool clip

        Returns:
            int: source end frame
        """
        return self._obj.GetSourceEndFrame()

    @property
    def source_start_time(self) -> float:
        """
        Returns the start time (seconds) of the used part of the media pool clip

        Returns:
            float: source start time
        """
        return self._obj.GetSourceStartTime()

    @property
    def source_end_time(self) -> float:
        """
        Returns the end time (seconds) of the used part of the media pool clip

        Returns:
            float: source end time
        """
        return self._obj.GetSourceEndTime()

    def set_left_offset(
        self, offset: float, subframe_precision: bool = False, update_linked_items: bool = True
    ) -> bool:
        """
        Trims the start of the clip so that ``offset`` frames are left to extend it (see ``left_offset``)

        Args:
            offset (float): available frames on the left
            subframe_precision (bool, optional): allow fractional offsets for audio. Defaults to ``False``.
            update_linked_items (bool, optional): trim linked items too. Defaults to ``True``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetLeftOffset(offset, subframe_precision, update_linked_items)

    def set_right_offset(
        self, offset: float, subframe_precision: bool = False, update_linked_items: bool = True
    ) -> bool:
        """
        Trims the end of the clip so that ``offset`` frames are left to extend it (see ``right_offset``)

        Args:
            offset (float): available frames on the right
            subframe_precision (bool, optional): allow fractional offsets for audio. Defaults to ``False``.
            update_linked_items (bool, optional): trim linked items too. Defaults to ``True``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetRightOffset(offset, subframe_precision, update_linked_items)

    def get_position(self, subframe_precision: bool = False) -> "TimelineItemPosition":
        """
        Returns the position of the item

        Args:
            subframe_precision (bool, optional): fractional ``startFrame``. Defaults to ``False``.

        Returns:
            dict: ``{"trackType": str, "trackIndex": int, "startFrame": float}``
        """
        return self._obj.GetPosition(subframe_precision)

    def set_position(
        self,
        position: "TimelineItemPosition",
        move_linked_items: bool = True,
        subframe_precision: bool = False,
    ) -> bool:
        """
        Moves the item

        Args:
            position (dict): ``{"trackIndex": int, "startFrame": float}``, omitted keys keep the current value
            move_linked_items (bool, optional): move linked items too. Defaults to ``True``.
            subframe_precision (bool, optional): allow fractional ``startFrame`` for audio. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetPosition(position, move_linked_items, subframe_precision)

    @property
    def track_type_and_index(self) -> Tuple[str, int]:
        """
        Returns the track of the item

        Returns:
            Tuple[str, int]: track type and track index, e.g. ``("video", 1)``
        """
        track_type, track_index = self._obj.GetTrackTypeAndIndex()
        return track_type, int(track_index)

    @property
    def linked_items(self) -> List["TimelineItem"]:
        """
        Returns the items linked to this one (e.g. the audio of a video clip)

        Returns:
            List[TimelineItem]: linked items
        """
        return [TimelineItem(x) for x in as_list(self._obj.GetLinkedItems())]

    def add_transition(self, options: "TransitionOptions") -> Optional["TimelineItem"]:
        """
        Adds a transition to the start or end of this item

        Args:
            options (dict): ``type`` (e.g. ``"Cross Dissolve"``), ``category`` (``"simple"``, ``"fusion"``, ``"ofx"``,
                ``"audio"``), ``position`` (``"start"``/``"end"``), ``alignment`` (``"left"``, ``"center"``,
                ``"right"``), ``duration`` (frames, optional)

        Returns:
            Optional[TimelineItem]: the transition, ``None`` if it failed
        """
        transition = self._obj.AddTransition(options)
        return TimelineItem(transition) if transition else None

    @property
    def speed(self) -> "SpeedOptions":
        """
        Returns the clip speed (keys ``Percentage``, ``PitchCorrection``, ``StretchKeyframesToFit``,
        ``RippleTimeline``)

        Returns:
            dict: speed options
        """
        return self._obj.GetSpeed()

    def set_speed(self, options: "SpeedOptions") -> bool:
        """
        Sets the clip speed

        Args:
            options (dict): ``Percentage`` (``0.0`` is a freeze frame), ``PitchCorrection``,
                ``StretchKeyframesToFit``, ``RippleTimeline``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetSpeed(options)

    @property
    def fades(self) -> "FadeInfo":
        """
        Returns the fade durations in frames (keys ``FadeIn``, ``FadeOut``)

        Returns:
            dict: fades
        """
        return self._obj.GetFades()

    def set_fades(self, fades: "FadeInfo") -> bool:
        """
        Sets the fade durations in frames

        Args:
            fades (dict): ``{"FadeIn": int, "FadeOut": int}``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetFades(fades)

    def export_frame(
        self, frame_offset: int = 0, options: Optional["ExportFrameOptions"] = None
    ) -> Dict[str, Any]:
        """
        Exports a frame of this item as a still image

        Args:
            frame_offset (int, optional): 0-based frame offset from the item start. Defaults to ``0``.
            options (dict, optional): ``outputType`` (``"file"`` or ``"encodedString"``), ``encodedImageFormat``,
                ``filePath``, ``maxDimension``. Defaults to a base64 encoded jpg.

        Returns:
            dict: ``success``, ``error`` and ``data`` (base64 image for ``"encodedString"``)
        """
        if options is None:
            return self._obj.ExportFrame(frame_offset)
        return self._obj.ExportFrame(frame_offset, options)

    def copy_attributes(
        self, timeline_items: List["TimelineItem"], options: "CopyAttributesOptions"
    ) -> bool:
        """
        Pastes the selected attributes of this item onto ``timeline_items`` (Edit page "Paste Attributes")

        Args:
            timeline_items (List[TimelineItem]): target items
            options (dict): attributes to paste, see ``CopyAttributesOptions`` in ``_resolve_stubs.pyi``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CopyAttributes(get_resolveobjs(timeline_items), options)

    def get_color_versions(self, type: Literal["local", "remote"]) -> List[str]:
        """
        Returns the names of the local or remote color versions

        Args:
            type (Literal['local', 'remote']): version type

        Returns:
            List[str]: version names
        """
        if type == "local":
            return as_list(self._obj.GetVersionNameList(0))
        elif type == "remote":
            return as_list(self._obj.GetVersionNameList(1))
        else:
            return []

    @property
    def current_color_version(self) -> Dict[str, Any]:
        """
        Returns the current color version (keys ``versionName``, ``versionType``: 0 - local, 1 - remote)

        Returns:
            dict: version info
        """
        return self._obj.GetCurrentVersion()

    @property
    def stereo_convergence_values(self) -> Dict[int, float]:
        """
        Returns the stereo convergence keyframes (offset -> value)

        Returns:
            dict: convergence values
        """
        return self._obj.GetStereoConvergenceValues()

    @property
    def stereo_left_floating_window_params(self) -> Dict[int, Dict[str, Any]]:
        """
        Returns the floating window keyframes of the left eye (offset -> params)

        Returns:
            dict: floating window params
        """
        return self._obj.GetStereoLeftFloatingWindowParams()

    @property
    def stereo_right_floating_window_params(self) -> Dict[int, Dict[str, Any]]:
        """
        Returns the floating window keyframes of the right eye (offset -> params)

        Returns:
            dict: floating window params
        """
        return self._obj.GetStereoRightFloatingWindowParams()

    @property
    def source_audio_channel_mapping(self) -> Dict[str, Any]:
        """
        Returns the source audio channel mapping, see ``MediaPoolItem.audio_mapping``

        Returns:
            dict: audio mapping (parsed from Resolve's JSON)
        """
        mapping = self._obj.GetSourceAudioChannelMapping()
        return json.loads(mapping) if mapping else {}

    def set_source_audio_channel_mapping(self, mapping: Union[str, Dict[str, Any]]) -> bool:
        """
        Sets the source audio channel mapping

        Args:
            mapping (Union[str, dict]): audio mapping (dict or JSON string)

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if not isinstance(mapping, str):
            mapping = json.dumps(mapping)
        return self._obj.SetSourceAudioChannelMapping(mapping)

    def analyze_audio_levels(self, standard: str) -> Dict[str, float]:
        """
        Measures the loudness of this audio item

        Args:
            standard (str): a mode of ``Timeline.normalize_audio_modes`` except the peak only modes

        Returns:
            dict: ``TruePeak`` (dBFS) and ``Integrated`` (LUFS), ``-100.0`` if nothing was measured
        """
        return self._obj.AnalyzeAudioLevels(standard)

    @property
    def voice_isolation_state(self) -> "VoiceIsolationState":
        """
        Returns the Voice Isolation state

        Returns:
            dict: ``{"isEnabled": bool, "amount": int}``
        """
        return self._obj.GetVoiceIsolationState()

    def set_voice_isolation_state(self, state: "VoiceIsolationState") -> bool:
        """
        Sets the Voice Isolation state

        Args:
            state (dict): ``{"isEnabled": bool, "amount": int}``, amount ``0`` to ``100``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetVoiceIsolationState(state)

    def ripple_delete_silence(self, options: Optional["RemoveSilenceOptions"] = None) -> bool:
        """
        Ripple deletes the silent parts of this audio item

        Args:
            options (dict, optional): ``threshold`` (dB), ``preHead``, ``postTail``, ``minimumToStrip`` (frames),
                ``crossFadeAudio``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if options is None:
            return self._obj.RippleDeleteSilence()
        return self._obj.RippleDeleteSilence(options)

    def update_sidecar(self) -> bool:
        """
        Updates the sidecar file of BRAW clips or the RMD file of R3D clips

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateSidecar()

    def create_magic_mask(self, mode: str) -> bool:
        """
        Creates a magic mask (Resolve Studio)

        Args:
            mode (str): ``"F"`` (forward), ``"B"`` (backward) or ``"BI"`` (bidirectional)

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CreateMagicMask(mode)

    def regenerate_magic_mask(self) -> bool:
        """
        Regenerates the magic mask

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RegenerateMagicMask()

    def stabilize(self) -> bool:
        """
        Stabilizes the clip

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.Stabilize()

    def smart_reframe(self) -> bool:
        """
        Performs Smart Reframe (Resolve Studio), poll ``Project.smart_reframe_status``. It repositions the subject
        within the existing frame - set the timeline resolution and ``"timelineInputResMismatchBehavior"`` to
        ``"scaleToCrop"`` first when reframing to another aspect ratio.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SmartReframe()

    @property
    def color_output_cache_enabled(self) -> bool:
        """
        Returns whether "Render Cache Color Output" is enabled

        Returns:
            bool: ``True`` if enabled
        """
        # Resolve 21.1.2 returns a CACHE_* value (0 / 1), not a bool as documented
        return self._obj.GetIsColorOutputCacheEnabled() == constants.CACHE_ENABLED

    def set_color_output_cache(self, enabled: Union[bool, str, float]) -> bool:
        """
        Enables or disables "Render Cache Color Output"

        Args:
            enabled (Union[bool, str, float]): ``True``/``False``, ``"enabled"``/``"disabled"`` or a ``CACHE_*``
                constant

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetColorOutputCache(_cache_mode(enabled))

    @property
    def fusion_output_cache(self) -> int:
        """
        Returns the "Render Cache Fusion Output" mode

        Returns:
            int: a ``CACHE_*`` constant: ``-1`` auto, ``0`` disabled, ``1`` enabled
        """
        # Resolve 21.1.2 returns the CACHE_* value, not a string as documented
        return self._obj.GetIsFusionOutputCacheEnabled()

    def set_fusion_output_cache(self, cache_value: Union[bool, str, float]) -> bool:
        """
        Sets "Render Cache Fusion Output"

        Args:
            cache_value (Union[bool, str, float]): ``"auto"``, ``"enabled"``, ``"disabled"``, ``True``/``False``
                or a ``CACHE_*`` constant

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetFusionOutputCache(_cache_mode(cache_value))

    @property
    def output_blanking(self) -> "OutputBlanking":
        """
        Returns the output blanking of the clip in pixels (keys ``Top``, ``Bottom``, ``Left``, ``Right``),
        empty if the timeline's output blanking is used

        Returns:
            dict: output blanking
        """
        return self._obj.GetOutputBlanking()

    def set_output_blanking(self, blanking: "OutputBlanking") -> bool:
        """
        Sets the output blanking of the clip in pixels

        Args:
            blanking (dict): keys ``Top``, ``Bottom``, ``Left``, ``Right``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetOutputBlanking(blanking)

    @property
    def use_timeline_output_blanking(self) -> bool:
        """
        Gets or sets whether the clip uses the timeline's output blanking

        Returns:
            bool: ``True`` if the timeline's output blanking is used
        """
        return self._obj.GetUseTimelineForOutputBlanking()

    @use_timeline_output_blanking.setter
    def use_timeline_output_blanking(self, use: bool) -> None:
        self._obj.SetUseTimelineForOutputBlanking(use)

    def perform_multicam_smart_switch(self, settings: "SmartSwitchSettings") -> bool:
        """
        Performs Multicam SmartSwitch on this multicam clip (Resolve Studio)

        Args:
            settings (dict): see ``SmartSwitchSettings`` in ``_resolve_stubs.pyi``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.PerformMulticamSmartSwitch(settings)

    def flatten_multicam(self, grade_option: Union[str, float]) -> bool:
        """
        Flattens this multicam clip

        Args:
            grade_option (Union[str, float]): ``"copy_grade"``, ``"retain_grade_from_angle"`` or a
                ``FLATTEN_MULTICAM_*`` constant

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.FlattenMulticam(constants.lookup("FLATTEN_MULTICAM_", grade_option))

    def __repr__(self) -> str:
        clip_repr = str(self.start) + "{| " + str(self.duration) + " |}" + str(self.end)
        return f'TimelineItem(Name:"{self.name}", In/Duration/Out: {clip_repr})'
