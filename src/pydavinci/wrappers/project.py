from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.exceptions import ObjectNotFound
from pydavinci.main import resolve_obj
from pydavinci.utils import as_list, get_resolveobj, is_resolve_obj
from pydavinci.wrappers.gallery import Gallery
from pydavinci.wrappers.settings.constructor import get_prj_settings

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import (
        CreateSubtitlesFromAudioStatus,
        DetectSceneCutsStatus,
        PhotoQuickExportRenderSettings,
        PhotoRenderSettings,
        PyRemoteProject,
        QuickExportRenderSettings,
        QuickExportRenderStatus,
        SlateAnalysisStatus,
        SmartReframeStatus,
        SpeechSettings,
        TranscribeAudioStatus,
    )
    from pydavinci.wrappers.colorgroup import ColorGroup
    from pydavinci.wrappers.mediapool import MediaPool
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem
    from pydavinci.wrappers.photoalbum import PhotoAlbum
    from pydavinci.wrappers.settings.constructor import ProjectSettings
    from pydavinci.wrappers.timeline import Timeline


class Project:
    def __init__(self, *args: Any) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj: "PyRemoteProject" = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            self._obj = resolve_obj.GetProjectManager().GetCurrentProject()

        self._settings: Optional["ProjectSettings"] = None

    @property
    def settings(self) -> "ProjectSettings":
        """Returns the [`ProjectSettings`](../settings/project) interface."""

        if self._settings is None:
            self._settings = get_prj_settings(self)
            return self._settings

        else:
            return self._settings

    @property
    def mediapool(self) -> "MediaPool":
        """Returns the
        [``MediaPool``][pydavinci.wrappers.mediapool.MediaPool-attributes] object.
        Returns:
            (MediaPool): Media Storage object
        """
        from pydavinci.wrappers.mediapool import MediaPool

        return MediaPool()

    @property
    def timeline_count(self) -> int:
        """
        Get total timeline count on current project

        Returns:
            timeline count
        """
        return self._obj.GetTimelineCount()

    @property
    def timelines(self) -> Union[list["Timeline"], None]:
        """
        Returns all timelines

        Returns:
            list[Timeline]: timelines
        """

        from pydavinci.wrappers.timeline import Timeline

        timelines = []
        count = self._obj.GetTimelineCount()
        for i in range(count):
            timelines.append(Timeline(self._obj.GetTimelineByIndex(i + 1)))

        return timelines if timelines else None

    @property
    def name(self) -> str:
        """
        Gets or sets current project name

        Returns:
            project name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> bool:
        """
        Project name. Use to rename project

        ``Project.name = 'New Project Name'``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetName(name)

    @property
    def presets(self) -> List[str]:
        """Gets a list of available project presets

        Returns:
            project presets
        """
        return self._obj.GetPresetList()

    def set_preset(self, preset_name: str) -> bool:
        """
        Activates ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetPreset(preset_name)

    def add_renderjob(self, block: bool = True) -> str:
        """
        Adds current render settings to a render job.

        If there are already rendered jobs in the render queue and you're executing a lot of commands, there's a bug on
        the Davinci API that there's a chance it will return an empty string instead of the job ID.

        ``block`` blocks the program until we get a job id back from Davinci Resolve. It's ``True`` by default.

        Returns:
            str: render job id
        """
        job_id = self._obj.AddRenderJob()

        if block and job_id == "":
            while job_id == "":
                job_id = self._obj.AddRenderJob()

            return job_id

        return job_id

    def delete_renderjob(self, job_id: str) -> bool:
        """
        Deletes render job ``job_id``

        Args:
            job_id (str): render job id

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteRenderJob(job_id)

    def delete_all_renderjobs(self) -> bool:
        """
        Deletes all renderjobs

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteAllRenderJobs()

    @property
    def render_jobs(self) -> List[str]:
        """
        Gets current list of render jobs

        Returns:
            list: render job list
        """
        return self._obj.GetRenderJobList()

    @property
    def render_presets(self) -> List[str]:
        """
        Gets available __render__ presets list

        Returns:
            list: available render presets list
        """
        return self._obj.GetRenderPresetList()

    def render(self, job_ids: Optional[List[str]] = None, interactive: bool = True) -> bool:
        """
        Render jobs

        Args:
            job_ids (Union[None, List[str]], optional): Renders provided list of ``job ids``. If ``None`` provided, render all jobs in queue. Defaults to ``None``.
            interactive (bool, optional): Whether to use interactive mode. When set to ``True``, enables error feedback in the UI during rendering.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        # TODO: the API supports passing only jobs ids: str as arguments. Implement here
        # using *args and update stub.
        if not job_ids:
            return self._obj.StartRendering(isInteractiveMode=interactive)
        else:
            return self._obj.StartRendering(job_ids, isInteractiveMode=interactive)

    def stop_render(self) -> None:
        """
        Stops all rendering.

        Returns:
            None: None
        """
        return self._obj.StopRendering()

    def render_status(self, job_id: str) -> Dict[Any, Union[str, int]]:
        """
        Gets render status on ``job_id``

        Args:
            job_id (str): job id

        Returns:
            dict: dictionary with render status

        Render Status:
            The dictionary returned looks like this when rendering:
            ```python
            {'JobStatus': 'Rendering',
            'CompletionPercentage': 92,
            'EstimatedTimeRemainingInMs': 1000}
            ```
            And like this when the render on the provided job id is complete:
            ```python
            {'JobStatus': 'Complete',
            'CompletionPercentage': 100,
            'TimeTakenToRenderInMs': 25991}
            ```
        """
        return self._obj.GetRenderJobStatus(job_id)

    @property
    def render_formats(self) -> Dict[Any, Any]:
        """
        Gets all possible render formats.

        Returns:
            dict: dict with render formats
        """
        return self._obj.GetRenderFormats()

    def get_render_codecs(self, render_format: str) -> Dict[Any, Any]:
        """Returns all possible render codecs.

        Args:
            render_format (str): render format

        Returns:
            Dict[Any, Any]: render codecs
        """
        return self._obj.GetRenderCodecs(render_format)

    @property
    def current_render_format_and_codec(self) -> Dict[Any, Any]:
        """
        Gets current render format and codec.

        Returns:
            dict: dict with current render format and codec
        """
        return self._obj.GetCurrentRenderFormatAndCodec()

    def set_render_format_and_codec(self, format: str, codec: str) -> bool:
        """
        Sets current ``format`` and ``codec``


        Args:
            format (str): render format
            codec (str): render codec

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCurrentRenderFormatAndCodec(format, codec)

    @property
    def render_mode(self) -> str:
        """Gets or sets current render mode. ``single`` for single clip and ``individual`` for individual clips.

        Returns:
            render mode ``single`` or ``individual``
        """
        if self._obj.GetCurrentRenderMode() == 1:
            return "single"
        else:
            return "individual"

    @render_mode.setter
    def render_mode(self, mode: str) -> bool:
        if "individual" in mode:
            return self._obj.SetCurrentRenderMode(0)
        elif "single" in mode:
            return self._obj.SetCurrentRenderMode(1)
        else:
            raise ValueError(
                'Render mode must be "single" or "individual", \
                for single clip and individual clips, respectively.'
            )

    def available_resolutions(
        self, format: Optional[str] = None, codec: Optional[str] = None
    ) -> List[Dict[Any, Any]]:
        """Returns list of resolutions applicable for the given render ``format`` and render ``codec``.

        Returns full list of resolutions if no argument is provided.
        Each element in the list is a dictionary with 2 keys "Width" and "Height".

        Args:
            format (str): render format
            codec (str): render codec

        Returns:
            List of available resolutions
        """
        if format is None and codec is None:
            return self._obj.GetRenderResolutions()
        else:
            return self._obj.GetRenderResolutions(format, codec)

    def is_rendering(self) -> bool:
        """
        Checks if DaVinci Resolve is rendering.

        Returns:
            bool: `True` if rendering, `False` otherwise
        """
        return self._obj.IsRenderingInProgress()

    def load_render_preset(self, preset_name: str) -> bool:
        """
        Loads render preset ``preset_name``.

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadRenderPreset(preset_name)

    def save_render_preset_as(self, preset_name: str) -> bool:
        """
        Save current preset as ``preset_name``.

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SaveAsNewRenderPreset(preset_name)

    def set_render_settings(self, render_settings: Dict[Any, Any]) -> bool:
        """
        Set render settings.

        Render Settings:
        ```python
            render_settings = {
            "SelectAllFrames": bool, # (when set True, the settings MarkIn and MarkOut are ignored)
            "MarkIn": int,
            "MarkOut": int,
            "TargetDir": str,
            "CustomName": str,
            "UniqueFilenameStyle": int, # 0 - Prefix, 1 - Suffix.
            "ExportVideo": bool,
            "ExportAudio": bool,
            "FormatWidth": int,
            "FormatHeight": int,
            "FrameRate": float, # (examples: 23.976, 24)
            "PixelAspectRatio": str, # (for SD resolution: "16_9" or "4_3") (other resolutions: "square" or "cinemascope")
            "VideoQuality": Union[int, str],
               # possible values for current codec (if applicable):
               # 0 (int) - will set quality to automatic
               # [1 -> MAX] (int) - will set input bit rate
               # ["Least", "Low", "Medium", "High", "Best"] (String) - will set input quality level
            "AudioCodec": str, # (example: "aac")
            "AudioBitDepth": int,
            "AudioSampleRate": int,
            "ColorSpaceTag" : str, # (example: "Same as Project", "AstroDesign")
            "GammaTag" : str, # (example: "Same as Project", "ACEScct")
            "ExportAlpha": bool,
            "EncodingProfile": str, # (example: "Main10"). Can only be set for H.264 and H.265.
            "MultiPassEncode": bool, # Can only be set for H.264.
            "AlphaMode": int, # 0 - Premultiplied, 1 - Straight. Can only be set if "ExportAlpha" is true.
            "NetworkOptimization": bool, # Only supported by QuickTime and MP4 formats.
        ```
        Args:
            render_settings (dict): dictionary with render settings

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetRenderSettings(render_settings)

    def get_setting(self, settingname: Optional[str] = None) -> Any:
        """
        Get project setting. If no setting provided, returns a dict with all settings.

        Args:
            setting (str): setting name

        Returns:
            dict: dict with setting name and value
        """
        if settingname:
            return self._obj.GetSetting(settingname)
        return self._obj.GetSetting()

    def set_setting(self, setting: str, value: Any) -> bool:
        """
        Set project setting.

        Args:
            setting (str): setting name
            value (Any): setting value

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetSetting(setting, value)

    def save(self) -> bool:
        """
        Saves project.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return resolve_obj.GetProjectManager().SaveProject()

    ## note: after loading the first project, it's impossible
    ## to close a project and go back to the window with only
    ## the project manager showing.
    ## It defaults to a 'Untitled Project', and you can't close it
    def close(self) -> bool:
        """
        Closes current project.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return resolve_obj.GetProjectManager().CloseProject(self._obj)

    def open_timeline(self, name: str) -> bool:
        """
        Opens timeline named ``name``.

        Args:
            name (str): timeline name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        from pydavinci.wrappers.timeline import Timeline

        count = self._obj.GetTimelineCount()
        for i in range(count):
            tl = Timeline(self._obj.GetTimelineByIndex(i + 1))
            if tl.name == name:
                return self._obj.SetCurrentTimeline(tl._obj)

        raise ObjectNotFound("Couldn't find timeline by name.")

    @property
    def timeline(self) -> "Timeline":
        """
        Returns current [``Timeline``][pydavinci.wrappers.timeline.Timeline-attributes] object

        Returns:
            Timeline(Timeline): timeline object
        """
        from pydavinci.wrappers.timeline import Timeline

        return Timeline(self._obj.GetCurrentTimeline())

    def refresh_luts(self) -> bool:
        """
        Refresh luts.

        Returns:
            None: None
        """
        return self._obj.RefreshLUTList()

    @property
    def gallery(self) -> "Gallery":
        """
        Returns the ``Gallery`` object.

        Returns:
            Gallery: The ``Gallery`` object
        """
        return Gallery(self._obj.GetGallery())

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `Project` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    # --- analysis jobs ---------------------------------------------------------------------------

    @property
    def transcribe_audio_status(self) -> "TranscribeAudioStatus":
        """
        Returns the status of the running ``transcribe_audio`` job (of a ``MediaPoolItem`` or ``Folder``)

        Returns:
            dict: ``JobStatus`` (``"Inactive"``, ``"Initializing"``, ``"Analyzing"``, ``"Cancelling"``,
            ``"Cancelled"``, ``"Complete"``), while analyzing also ``CompletionPercentage``, ``CurrentClipIndex``,
            ``TotalClips``, ``EstimatedTimeRemaining`` (seconds), on failure ``Error``
        """
        return self._obj.GetTranscribeAudioStatus()

    @property
    def analyze_for_slate_status(self) -> "SlateAnalysisStatus":
        """
        Returns the status of the running ``analyze_for_slate`` job

        Returns:
            dict: ``JobStatus`` (... ``"Complete"`` or ``"Failed"``), ``CompletionPercentage``, ``CurrentClipIndex``,
            ``TotalClips``, ``EstimatedTimeRemaining``, ``Error``
        """
        return self._obj.GetAnalyzeForSlateStatus()

    @property
    def smart_reframe_status(self) -> "SmartReframeStatus":
        """
        Returns the status of the running ``TimelineItem.smart_reframe`` job

        Returns:
            dict: ``JobStatus``, ``CompletionPercentage``, ``AnalysisSpeed``, ``EstimatedTimeRemaining``, ``Error``
        """
        return self._obj.GetSmartReframeStatus()

    @property
    def detect_scene_cuts_status(self) -> "DetectSceneCutsStatus":
        """
        Returns the status of the running ``Timeline.detect_scene_cuts`` job

        Returns:
            dict: ``JobStatus``, ``CompletionPercentage``, ``AnalysisSpeed``, ``EstimatedTimeRemaining``
        """
        return self._obj.GetDetectSceneCutsStatus()

    @property
    def create_subtitles_from_audio_status(self) -> "CreateSubtitlesFromAudioStatus":
        """
        Returns the status of the running ``Timeline.create_subtitles_from_audio`` job

        Returns:
            dict: ``JobStatus``, ``CompletionPercentage``, ``AnalysisSpeed``, ``EstimatedTimeRemaining``, ``Error``
        """
        return self._obj.GetCreateSubtitlesFromAudioStatus()

    def reset_intellisearch_analysis(self) -> bool:
        """
        Resets the IntelliSearch analysis of the project

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ResetIntellisearchAnalysis()

    # --- settings and presets --------------------------------------------------------------------

    def get_settings(self) -> Dict[str, Any]:
        """
        Returns all project settings - the current form of ``get_setting()``, see ``ProjectSettings``
        in ``_resolve_stubs.pyi`` for keys and values

        Returns:
            dict: project settings
        """
        return self._obj.GetSettings()

    def set_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Sets project settings, e.g. ``{"timelineFrameRate": "25"}``. Settings are applied one by one: on failure the
        ones applied before are kept.

        Args:
            settings (dict): setting names and values

        Returns:
            bool: ``True`` if all were set, ``False`` otherwise
        """
        return self._obj.SetSettings(settings)

    @property
    def project_settings_presets(self) -> List[Dict[str, Any]]:
        """
        Returns the project settings presets (keys ``Name``, ``Width``, ``Height``)

        Returns:
            List[dict]: presets
        """
        return as_list(self._obj.GetProjectSettingsPresetList())

    def set_project_settings_preset(self, preset_name: str) -> bool:
        """
        Applies project settings preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetProjectSettingsPreset(preset_name)

    def save_project_settings_preset_as(self, preset_name: str) -> bool:
        """
        Saves the current project settings as new preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SaveCurrentProjectSettingsAsNewPreset(preset_name)

    def update_project_settings_preset(self, preset_name: str) -> bool:
        """
        Updates project settings preset ``preset_name`` with the current settings

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateProjectSettingsPreset(preset_name)

    def delete_project_settings_preset(self, preset_name: str) -> bool:
        """
        Deletes project settings preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteProjectSettingsPreset(preset_name)

    def export_project_settings_preset(self, preset_name: str, path: str) -> bool:
        """
        Exports project settings preset ``preset_name`` to ``path``

        Args:
            preset_name (str): preset name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportProjectSettingsPreset(preset_name, path)

    def import_project_settings_preset(self, path: str, preset_name: Optional[str] = None) -> bool:
        """
        Imports a project settings preset from ``path``

        Args:
            path (str): preset file path
            preset_name (str, optional): preset name. Defaults to the file name.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if preset_name is None:
            return self._obj.ImportProjectSettingsPreset(path)
        return self._obj.ImportProjectSettingsPreset(path, preset_name)

    def load_burn_in_preset(self, preset_name: str) -> bool:
        """
        Loads the user defined data burn-in preset ``preset_name`` for the project

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadBurnInPreset(preset_name)

    # --- rendering -------------------------------------------------------------------------------

    def delete_render_preset(self, preset_name: str) -> bool:
        """
        Deletes render preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteRenderPreset(preset_name)

    def update_render_preset(self, preset_name: str) -> bool:
        """
        Updates render preset ``preset_name`` with the current render settings

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateRenderPreset(preset_name)

    def set_quick_export_enabled(self, preset_name: str, enabled: bool) -> bool:
        """
        Enables or disables Quick Export for render preset ``preset_name``

        Args:
            preset_name (str): render preset name
            enabled (bool): ``True`` to enable

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetQuickExportEnabledForRenderPreset(preset_name, enabled)

    @property
    def quick_export_presets(self) -> List[str]:
        """
        Returns the Quick Export render presets

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetQuickExportRenderPresets())

    def render_with_quick_export(
        self, preset_name: str, settings: Optional["QuickExportRenderSettings"] = None
    ) -> "QuickExportRenderStatus":
        """
        Renders the current timeline with Quick Export preset ``preset_name``

        Args:
            preset_name (str): Quick Export preset name
            settings (dict, optional): ``TargetDir``, ``CustomName``, ``VideoQuality``, ``EnableUpload``

        Returns:
            dict: render status, see ``quick_export_status``
        """
        return self._obj.RenderWithQuickExport(preset_name, settings or {})

    @property
    def quick_export_status(self) -> "QuickExportRenderStatus":
        """
        Returns the status of the running ``render_with_quick_export``

        Returns:
            dict: ``JobStatus``, ``CompletionPercentage``, ``TimeTakenToRenderInMs``, ``EstimatedTimeRemainingInMs``,
            ``Error``
        """
        return self._obj.GetRenderWithQuickExportStatus()

    @property
    def photo_quick_export_presets(self) -> List[str]:
        """
        Returns the Quick Export render presets for photo albums

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetPhotoQuickExportRenderPresets())

    def set_photo_render_settings(self, settings: "PhotoRenderSettings") -> bool:
        """
        Sets render settings for the current photo album, settings not given keep their value
        (see ``PhotoRenderSettings`` in ``_resolve_stubs.pyi``)

        Args:
            settings (dict): photo render settings

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetPhotoRenderSettings(settings)

    def render_photos_with_quick_export(
        self, preset_name: str, settings: "PhotoQuickExportRenderSettings"
    ) -> "QuickExportRenderStatus":
        """
        Renders the current photo album with Quick Export preset ``preset_name``. Needs the Photo page
        (``Resolve.page = "photo"``), otherwise the status is ``"Render Failed"``.

        Args:
            preset_name (str): photo Quick Export preset name
            settings (dict): ``TargetDir`` and ``CustomName`` (required), ``BitDepth``, ``ManualQualityPercent``, ...
                see ``PhotoQuickExportRenderSettings`` in ``_resolve_stubs.pyi``

        Returns:
            dict: render status
        """
        return self._obj.RenderPhotosWithQuickExport(preset_name, settings)

    @property
    def audio_render_formats(self) -> Dict[str, str]:
        """
        Returns the audio render formats (format -> file extension)

        Returns:
            dict: audio render formats
        """
        return self._obj.GetAudioRenderFormats()

    def get_audio_render_codecs(self, audio_format: str) -> Dict[str, str]:
        """
        Returns the audio codecs of ``audio_format`` (codec description -> codec name)

        Args:
            audio_format (str): audio render format file extension

        Returns:
            dict: audio codecs
        """
        return self._obj.GetAudioRenderCodecs(audio_format)

    # --- photo albums ----------------------------------------------------------------------------

    @property
    def photo_albums(self) -> List["PhotoAlbum"]:
        """
        Returns all photo albums of the project

        Returns:
            List[PhotoAlbum]: photo albums
        """
        from pydavinci.wrappers.photoalbum import PhotoAlbum

        albums = [self._obj.GetPhotoAlbumByIndex(i + 1) for i in range(self._obj.GetPhotoAlbumCount())]
        return [PhotoAlbum(x) for x in albums if x]

    @property
    def photo_album(self) -> Optional["PhotoAlbum"]:
        """
        Returns the current photo album

        Returns:
            Optional[PhotoAlbum]: current photo album, ``None`` if there is none
        """
        from pydavinci.wrappers.photoalbum import PhotoAlbum

        album = self._obj.GetCurrentPhotoAlbum()
        return PhotoAlbum(album) if album else None

    def set_current_photo_album(self, photo_album: "PhotoAlbum") -> bool:
        """
        Makes ``photo_album`` the current photo album

        Args:
            photo_album (PhotoAlbum): photo album

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetCurrentPhotoAlbum(get_resolveobj(photo_album))

    # --- color groups ----------------------------------------------------------------------------

    @property
    def color_groups(self) -> List["ColorGroup"]:
        """
        Returns all color groups of the project

        Returns:
            List[ColorGroup]: color groups
        """
        from pydavinci.wrappers.colorgroup import ColorGroup

        return [ColorGroup(x) for x in as_list(self._obj.GetColorGroupsList())]

    def add_color_group(self, group_name: str) -> Optional["ColorGroup"]:
        """
        Creates color group ``group_name`` (must be unique)

        Args:
            group_name (str): group name

        Returns:
            Optional[ColorGroup]: created color group, ``None`` if it failed
        """
        from pydavinci.wrappers.colorgroup import ColorGroup

        group = self._obj.AddColorGroup(group_name)
        return ColorGroup(group) if group else None

    def delete_color_group(self, color_group: "ColorGroup") -> bool:
        """
        Deletes ``color_group``, its clips become ungrouped

        Args:
            color_group (ColorGroup): color group

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteColorGroup(get_resolveobj(color_group))

    # --- audio and stills ------------------------------------------------------------------------

    def insert_audio_at_playhead(
        self, media_path: str, start_offset_samples: int, duration_samples: int
    ) -> bool:
        """
        Inserts audio media into the current track at the playhead (Fairlight page)

        Args:
            media_path (str): audio file path
            start_offset_samples (int): start offset in samples
            duration_samples (int): duration in samples

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.InsertAudioToCurrentTrackAtPlayhead(
            media_path, start_offset_samples, duration_samples
        )

    def apply_fairlight_preset(self, preset_name: str) -> bool:
        """
        Applies Fairlight preset ``preset_name`` to the current timeline, see ``Resolve.fairlight_presets``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ApplyFairlightPresetToCurrentTimeline(preset_name)

    def generate_speech(
        self, settings: "SpeechSettings", timecode: Optional[str] = None
    ) -> Optional["MediaPoolItem"]:
        """
        Generates speech audio (Resolve Studio, Extras download "AI Speech Generator") into the current project
        and timeline

        Args:
            settings (dict): ``TextInput`` (max 350 characters), ``VoiceModel``, ``Speed``, ``Pitch``, ``Filename``,
                ``AddToTimeline``, ``AudioTrack``, ... see ``SpeechSettings`` in ``_resolve_stubs.pyi``
            timecode (str, optional): timeline position, used if ``AddToTimeline`` is set

        Returns:
            Optional[MediaPoolItem]: generated clip, ``None`` if it failed
        """
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        if timecode is None:
            item = self._obj.GenerateSpeech(settings)
        else:
            item = self._obj.GenerateSpeech(settings, timecode)
        return MediaPoolItem(item) if item else None

    def export_current_frame_as_still(self, path: str) -> bool:
        """
        Exports the current frame as still image to ``path``

        Args:
            path (str): target file path, the format follows the extension

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportCurrentFrameAsStill(path)

    def __repr__(self) -> str:
        return f'Project(Name: "{self.name})"'
