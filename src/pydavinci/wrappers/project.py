from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.exceptions import ObjectNotFound
from pydavinci.main import resolve_obj
from pydavinci.utils import is_resolve_obj
from pydavinci.wrappers.settings.constructor import get_prj_settings

from pydavinci.wrappers.gallery import Gallery

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteProject
    from pydavinci.wrappers.mediapool import MediaPool
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
        if format and codec is None:
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

    def __repr__(self) -> str:
        return f'Project(Name: "{self.name})"'
