from typing import TYPE_CHECKING, List, Optional, Union

from pydavinci.utils import as_list, is_resolve_obj
from pydavinci.wrappers import constants

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import DeblurOptions, PyRemoteFolder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem


class Folder:
    def __init__(self, obj: "PyRemoteFolder") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteFolder" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def clips(self) -> List[MediaPoolItem]:
        """
        Gets all clips

        Returns:
            (List[MediaPoolItem]): list of clips
        """
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        objs = as_list(self._obj.GetClipList())
        return [MediaPoolItem(x) for x in objs]

    @property
    def name(self) -> str:
        """
        Gets folder name

        Returns:
            name(str): folder name
        """
        return self._obj.GetName()

    @property
    def subfolders(self) -> List["Folder"]:
        """
        Gets subfolders

        Returns:
            subfolders(List[Folder]): subfolders
        """
        return [Folder(x) for x in as_list(self._obj.GetSubFolderList())]

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `Folder` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    @property
    def parent_folder(self) -> Optional["Folder"]:
        """
        Gets the parent folder

        Returns:
            Optional[Folder]: parent folder, ``None`` for the root folder
        """
        parent = self._obj.GetParentFolder()
        return Folder(parent) if parent else None

    @property
    def is_stale(self) -> bool:
        """
        Returns whether this folder is stale in collaboration mode (see ``MediaPool.refresh_folders``)

        Returns:
            bool: ``True`` if stale
        """
        return self._obj.GetIsFolderStale()

    def export(self, path: str) -> bool:
        """
        Exports this folder as a ``.drb`` file

        Args:
            path (str): target ``.drb`` file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.Export(path)

    def transcribe_audio(
        self, speaker_detection: Optional[bool] = None, as_nested_clip: bool = False
    ) -> bool:
        """
        Starts the audio transcription of all clips in this folder and its subfolders (Resolve Studio). It runs in the
        background - poll ``Project.transcribe_audio_status``, see ``MediaPoolItem.transcribe_audio``.

        Args:
            speaker_detection (bool, optional): detect speakers. Defaults to Resolve's setting.
            as_nested_clip (bool, optional): transcribe timeline clips as nested clips. Defaults to ``False``.

        Returns:
            bool: ``True`` if the transcription was started, ``False`` otherwise
        """
        if as_nested_clip:
            return self._obj.TranscribeAudio(speaker_detection, True)
        if speaker_detection is not None:
            return self._obj.TranscribeAudio(speaker_detection)
        return self._obj.TranscribeAudio()

    def clear_transcription(self) -> bool:
        """
        Clears the transcription of all clips in this folder and its subfolders

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearTranscription()

    def perform_audio_classification(self) -> bool:
        """
        Classifies the audio of all clips in this folder and its subfolders (Resolve Studio),
        see ``MediaPoolItem.perform_audio_classification``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.PerformAudioClassification()

    def clear_audio_classification(self) -> bool:
        """
        Clears the audio classification of all clips in this folder and its subfolders

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ClearAudioClassification()

    def analyze_for_intellisearch(self, identify_faces: bool = False, better_mode: bool = False) -> bool:
        """
        Performs IntelliSearch analysis on all clips in this folder (Resolve Studio),
        see ``MediaPoolItem.analyze_for_intellisearch``

        Args:
            identify_faces (bool, optional): identify faces. Defaults to ``False``.
            better_mode (bool, optional): better instead of faster analysis. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AnalyzeForIntellisearch(identify_faces, better_mode)

    def analyze_for_slate(self, marker_color: Union[str, float]) -> bool:
        """
        Starts the slate analysis of all clips in this folder (Resolve Studio), see
        ``MediaPoolItem.analyze_for_slate``. Poll ``Project.analyze_for_slate_status``.

        Args:
            marker_color (Union[str, float]): marker color (``"Blue"``, ``"Red"``, ...) or a ``MARKER_*`` constant

        Returns:
            bool: ``True`` if the analysis was started, ``False`` otherwise
        """
        return self._obj.AnalyzeForSlate(constants.lookup("MARKER_", marker_color))

    def remove_motion_blur(
        self, options: Optional["DeblurOptions"] = None
    ) -> List[List[MediaPoolItem]]:
        """
        Renders motion deblurred copies of the clips in this folder (Resolve Studio),
        see ``MediaPoolItem.remove_motion_blur``

        Args:
            options (dict, optional): deblur options. Defaults to Resolve's defaults.

        Returns:
            List[List[MediaPoolItem]]: pairs of original and new clip
        """
        if options is None:
            result = self._obj.RemoveMotionBlur()
        else:
            result = self._obj.RemoveMotionBlur(options)
        return [[MediaPoolItem(x) for x in as_list(pair) if x] for pair in as_list(result)]

    def __repr__(self) -> str:
        return f'Folder(Name:"{self.name})"'
