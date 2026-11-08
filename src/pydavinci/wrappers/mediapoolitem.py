import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers import constants
from pydavinci.wrappers.marker import MarkerCollection

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import (
        DeblurOptions,
        ExportFrameOptions,
        PyRemoteMediaPoolItem,
        Transcription,
    )
    from pydavinci.wrappers.folder import Folder
    from pydavinci.wrappers.photoalbum import PhotoAlbum
    from pydavinci.wrappers.timeline import Timeline

MARK_TYPES = ["video", "audio", "all"]


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
        Gets or sets the ``MediaPoolItem`` name (the clip name, not the file name).
        Use [``set_name``][pydavinci.wrappers.mediapoolitem.MediaPoolItem.set_name] to check the result.

        Returns:
            (str): ``MediaPoolItem`` name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> None:
        self._obj.SetName(name)

    def set_name(self, name: str) -> bool:
        """
        Sets the clip name

        Args:
            name (str): new clip name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetName(name)

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

    def link_full_resolution_media(self, path: str) -> bool:
        """
        Links the full resolution media at ``path`` to this clip, for clips that were imported from their
        proxy media (the counterpart of [``link_proxy``][pydavinci.wrappers.mediapoolitem.MediaPoolItem.link_proxy])

        Args:
            path (str): _absolute_ path to the full resolution media

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LinkFullResolutionMedia(path)

    def replace_clip_preserve_subclip(self, path: str) -> bool:
        """
        Like [``replace_clip``][pydavinci.wrappers.mediapoolitem.MediaPoolItem.replace_clip], but keeps the
        extents of a subclip

        Args:
            path (str): path to clip

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ReplaceClipPreserveSubClip(path)

    @property
    def parent_folder(self) -> "Folder":
        """
        Returns the ``Folder`` (bin) containing this clip

        Returns:
            Folder: parent folder
        """
        from pydavinci.wrappers.folder import Folder

        return Folder(self._obj.GetParentFolder())

    @property
    def timeline(self) -> Optional["Timeline"]:
        """
        Returns the ``Timeline`` of a timeline clip

        Returns:
            Optional[Timeline]: timeline, ``None`` if this is no timeline clip
        """
        from pydavinci.wrappers.timeline import Timeline

        timeline = self._obj.GetTimeline()
        return Timeline(timeline) if timeline else None

    @property
    def photo_album(self) -> Optional["PhotoAlbum"]:
        """
        Returns the ``PhotoAlbum`` of a photo album clip

        Returns:
            Optional[PhotoAlbum]: photo album, ``None`` if this is no photo album clip
        """
        from pydavinci.wrappers.photoalbum import PhotoAlbum

        album = self._obj.GetPhotoAlbum()
        return PhotoAlbum(album) if album else None

    def get_third_party_metadata(
        self, metadata_key: Optional[str] = None
    ) -> Union[str, Dict[Any, Any]]:
        """
        Gets third party metadata ``metadata_key`` - custom keys that are not part of Resolve's metadata.
        If no ``metadata_key`` is provided, returns a ``Dict`` with all third party metadata.

        Args:
            metadata_key (str, optional): metadata key

        Returns:
            (Union[str, Dict[Any, Any]]): value of ``metadata_key`` (empty if not set) or ``Dict`` with all values
        """
        if metadata_key:
            return self._obj.GetThirdPartyMetadata(metadata_key)
        return self._obj.GetThirdPartyMetadata()

    def set_third_party_metadata(self, meta_dict: Dict[str, str]) -> bool:
        """
        Sets or adds third party metadata - any key, values are strings:
        ```python
            meta_dict = {"liquit_shot": "sh010"}
        ```

        Args:
            meta_dict (dict): dict with metadata to be set

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetThirdPartyMetadata(meta_dict)

    def export_frame(
        self, frame_offset: int = 0, options: Optional["ExportFrameOptions"] = None
    ) -> Dict[str, Any]:
        """
        Exports a frame of this clip as a still image

        Args:
            frame_offset (int, optional): 0-based frame offset from the clip start. Defaults to ``0``.
            options (dict, optional): ``outputType`` (``"file"`` or ``"encodedString"``), ``encodedImageFormat``
                (``"jpg"``/``"png"``), ``filePath``, ``maxDimension``. Defaults to a base64 encoded jpg.

        Returns:
            dict: ``success``, ``error`` and ``data`` (base64 image for ``"encodedString"``)
        """
        if options is None:
            return self._obj.ExportFrame(frame_offset)
        return self._obj.ExportFrame(frame_offset, options)

    def transcribe_audio(
        self, speaker_detection: Optional[bool] = None, as_nested_clip: bool = False
    ) -> bool:
        """
        Starts the audio transcription of this clip. It runs in the background (Resolve Studio) -
        poll [``Project.transcribe_audio_status``][pydavinci.wrappers.project.Project.transcribe_audio_status]
        until its ``JobStatus`` is ``"Complete"``, then read [``get_transcription``][pydavinci.wrappers.mediapoolitem.MediaPoolItem.get_transcription].

        The transcription language is the one of the project settings.

        Args:
            speaker_detection (bool, optional): detect speakers. Defaults to Resolve's setting.
            as_nested_clip (bool, optional): transcribe a timeline clip as nested clip. Defaults to ``False``.

        Returns:
            bool: ``True`` if the transcription was started, ``False`` otherwise
        """
        if as_nested_clip:
            return self._obj.TranscribeAudio(speaker_detection, True)
        if speaker_detection is not None:
            return self._obj.TranscribeAudio(speaker_detection)
        return self._obj.TranscribeAudio()

    def get_transcription(self, nested_clip: bool = False) -> Optional["Transcription"]:
        """
        Returns the transcription of this clip

        Transcription:
            ```python
            {
                "language": "en",
                "segments": [
                    {
                        "start": "10:00:01:05",  # timecode
                        "end": "10:00:09:00",
                        "text": " Hello, this is a test.",  # words joined, "(...)" is silence
                        "speaker": "Speaker 1",  # if speakers were detected
                        "words": [{"start": "10:00:01:05", "end": "10:00:01:13", "text": " Hello,"}, ...],
                    },
                ],
            }
            ```

        Args:
            nested_clip (bool, optional): the transcription of a timeline clip as nested clip. Defaults to ``False``.

        Returns:
            Optional[dict]: transcription, ``None`` if the clip has none
        """
        if nested_clip:
            return self._obj.GetTranscription(True)
        return self._obj.GetTranscription()

    def set_transcription(self, transcription: "Transcription") -> bool:
        """
        Replaces the transcription of this clip (Resolve Studio), e.g. a corrected one from
        [``get_transcription``][pydavinci.wrappers.mediapoolitem.MediaPoolItem.get_transcription].

        Rules:
            - ``segments`` must not be empty - use ``clear_transcription`` instead
            - each segment needs a non-empty ``words`` list, each word a ``text``. Word texts are joined as they are:
              start them with a space like Resolve does (``" world"``)
            - a segment needs ``start`` and ``end`` unless its first and last word have timecodes; words without
              timecodes are spread evenly over the gaps, and Resolve 21.1.2 then reports the space between them as
              silence words ``"(...)"`` - pass word timecodes to get the text back unchanged
            - segments and words in ascending order, segments must not overlap; gaps become silence ``"(...)"``
            - ``language`` and ``speaker`` are optional, unknown speakers are added to the project

        Args:
            transcription (dict): transcription, see ``get_transcription``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetTranscription(transcription)

    def clear_transcription(self, nested_clip: bool = False) -> bool:
        """
        Clears the transcription of this clip

        Args:
            nested_clip (bool, optional): clear the nested clip transcription of a timeline clip. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if nested_clip:
            return self._obj.ClearTranscription(True)
        return self._obj.ClearTranscription()

    def perform_audio_classification(self) -> bool:
        """
        Classifies the audio of this clip (Resolve Studio). The result is in the clip properties ``"Category"``
        and ``"Subcategory"`` (e.g. ``"Dialogue"``).

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.PerformAudioClassification()

    def clear_audio_classification(self) -> bool:
        """
        Clears the audio classification of this clip

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearAudioClassification()

    def analyze_for_intellisearch(self, identify_faces: bool = False, better_mode: bool = False) -> bool:
        """
        Performs IntelliSearch analysis on this clip (Resolve Studio). Requires the Extras download
        "AI IntelliSearch - Faster" (``better_mode=False``) or "- Better" (``better_mode=True``).

        Args:
            identify_faces (bool, optional): identify faces. Defaults to ``False``.
            better_mode (bool, optional): better instead of faster analysis. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AnalyzeForIntellisearch(identify_faces, better_mode)

    def analyze_for_slate(self, marker_color: Union[str, float]) -> bool:
        """
        Starts the slate analysis of this clip (Resolve Studio, Extras download "AI IntelliSearch - Faster").
        Each slate found gets a "Detected Slate" duration marker in ``marker_color`` - the text on the slate is not read.
        Poll [``Project.analyze_for_slate_status``][pydavinci.wrappers.project.Project.analyze_for_slate_status].

        Args:
            marker_color (Union[str, float]): marker color (``"Blue"``, ``"Red"``, ...) or a ``MARKER_*`` constant

        Returns:
            bool: ``True`` if the analysis was started, ``False`` otherwise
        """
        return self._obj.AnalyzeForSlate(constants.lookup("MARKER_", marker_color))

    @property
    def audio_mapping(self) -> Dict[str, Any]:
        """
        Returns the audio mapping of this clip: embedded channels, linked audio (e.g. after
        ``MediaPool.auto_sync_audio``) and track mapping

        Returns:
            dict: audio mapping (parsed from Resolve's JSON)
        """
        mapping = self._obj.GetAudioMapping()
        return json.loads(mapping) if mapping else {}

    def set_audio_mapping(self, mapping: Union[str, Dict[str, Any]]) -> bool:
        """
        Sets the audio mapping of this clip

        Args:
            mapping (Union[str, dict]): audio mapping as returned by ``audio_mapping`` (dict or JSON string)

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if not isinstance(mapping, str):
            mapping = json.dumps(mapping)
        return self._obj.SetAudioMapping(mapping)

    @property
    def mark_in_out(self) -> Dict[str, Dict[str, int]]:
        """
        Returns the in/out marks of this clip

        Returns:
            dict: ``{"video": {"in": int, "out": int}, "audio": {...}}``, empty dicts if not set
        """
        return self._obj.GetMarkInOut()

    def set_mark_in_out(self, mark_in: int, mark_out: int, mark_type: str = "all") -> bool:
        """
        Sets the in/out marks of this clip

        Args:
            mark_in (int): in frame
            mark_out (int): out frame
            mark_type (str, optional): ``"video"``, ``"audio"`` or ``"all"``. Defaults to ``"all"``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if mark_type not in MARK_TYPES:
            raise ValueError(f"Mark type must be one of {MARK_TYPES}")
        return self._obj.SetMarkInOut(mark_in, mark_out, mark_type)

    def clear_mark_in_out(self, mark_type: str = "all") -> bool:
        """
        Clears the in/out marks of this clip

        Args:
            mark_type (str, optional): ``"video"``, ``"audio"`` or ``"all"``. Defaults to ``"all"``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if mark_type not in MARK_TYPES:
            raise ValueError(f"Mark type must be one of {MARK_TYPES}")
        return self._obj.ClearMarkInOut(mark_type)

    def monitor_growing_file(self) -> bool:
        """
        Keeps monitoring this clip's file while it is growing

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.MonitorGrowingFile()

    def remove_motion_blur(self, options: "DeblurOptions") -> Optional["MediaPoolItem"]:
        """
        Renders a motion deblurred copy of this clip (Resolve Studio)

        Args:
            options (dict): ``FileName``, ``Format``, ``Codec``, ``EncodingProfile``, ``Encoder``, ``UseExtremeMode``,
                ``UseMarkInMarkOut``, ``RenderAtSourceRes``, ``UseMoreGpuMemory`` - see ``DeblurOptions``
                in ``_resolve_stubs.pyi``

        Returns:
            Optional[MediaPoolItem]: the new clip, ``None`` if it failed
        """
        item = self._obj.RemoveMotionBlur(options)
        return MediaPoolItem(item) if item else None

    def __repr__(self) -> str:
        return f'MediaPoolItem(Name:"{self.name})"'
