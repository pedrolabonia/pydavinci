from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydavinci.exceptions import ObjectNotFound
from pydavinci.main import resolve_obj
from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteProject
    from pydavinci.wrappers.mediapool import MediaPool
    from pydavinci.wrappers.timeline import Timeline


class Project(object):
    def __init__(self, *args: "PyRemoteProject") -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            self._obj = resolve_obj.GetProjectManager().GetCurrentProject()

    @property
    def mediapool(self) -> "MediaPool":
        """
        Returns:
            MediaPool: media pool object
        """
        from pydavinci.wrappers.mediapool import MediaPool

        return MediaPool()

    @property
    def timeline_count(self) -> int:
        """
        Get total timeline count on current project

        Returns:
            int: timeline count
        """
        return self._obj.GetTimelineCount()

    @property
    def name(self) -> str:
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

    def add_renderjob(self) -> str:
        """
        Adds current render settings to a render job

        Returns:
            str: render job id
        """
        return self._obj.AddRenderJob()

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
        Gets current render job list

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

    def render(self, job_ids: Optional[List[str]] = None, interactive: bool = False) -> bool:
        """
        Render jobs

        Args:
            job_ids (Union[None, List[str]], optional): Renders provided list of ``job ids``. If ``None`` provided, render all jobs in queue. Defaults to ``None``.
            interactive (bool, optional): Whether to use interactive mode. ``False`` provides better results when rendering programatically. Defaults to False.

        Returns:
            bool: _description_
        """
        # TODO: the API supports passing only jobs ids: str as arguments. Implement here
        # using *args and update stub.
        if not job_ids:
            return self._obj.StartRendering(isInteractiveMode=interactive)
        else:
            return self._obj.StartRendering(job_ids, isInteractiveMode=interactive)

    def stop_render(self) -> None:
        """
        Stops all rendering

        Returns:
            None: None
        """
        return self._obj.StopRendering()

    def render_status(self, job_id: str) -> Dict[Any, Any]:
        """
        Gets render status on ``job_id``

        Args:
            job_id (str): job id

        Returns:
            dict: dictionary with render status

        Info:
            The dictionary returned looks like this when rendering:
            ```python
            {'JobStatus': 'Rendering',
            'CompletionPercentage': 92,
            'EstimatedTimeRemainingInMs': 1000}
            ```
            And like this when the render is complete:
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
        Gets all possible render formats

        Returns:
            dict: dict with render formats
        """
        return self._obj.GetRenderFormats()

    def get_render_codecs(self, render_format: str) -> Dict[Any, Any]:
        return self._obj.GetRenderCodecs(render_format)

    @property
    def current_render_format_and_codec(self) -> Dict[Any, Any]:
        """
        Gets current render format and codec

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
    def render_mode(self) -> int:
        return self._obj.GetCurrentRenderMode()

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

    def available_resolutions(self, format: str, codec: str) -> List[Dict[Any, Any]]:
        return self._obj.GetRenderResolutions(format, codec)

    @property
    def rendering(self) -> bool:
        """
        Checks if Davinci is rendering

        Returns:
            bool: `True` if rendering, `False` otherwise
        """
        return self._obj.IsRenderingInProgress()

    def load_render_preset(self, preset_name: str) -> bool:
        """
        Loads render preset

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadRenderPreset(preset_name)

    def save_render_preset_as(self, preset_name: str) -> bool:
        """
        Save current preset as ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SaveAsNewRenderPreset(preset_name)

    def set_render_settings(self, render_settings: Dict[Any, Any]) -> bool:
        """
        Set render settins

        Args:
            render_settings (dict): dictionary with render settings

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetRenderSettings(render_settings)

    def get_setting(self, setting: str) -> Any:
        """
        Get Setting

        Args:
            setting (str): setting name

        Returns:
            dict: dict with setting name and value
        """
        return self._obj.GetSetting(setting)

    def set_setting(self, setting: str, value: str) -> bool:
        """
        Set Setting

        Args:
            setting (str): setting name
            value (str): setting value, stringfied

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetSetting(setting, value)

    def save(self) -> bool:
        """
        Saves project

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
        Closes project

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return resolve_obj.GetProjectManager().CloseProject(self._obj)

    def open_timeline(self, name: str) -> bool:
        """
        Opens timeline named ``name``

        Args:
            name (str): timeline name

        Raises:
            ObjectNotFound: Can't find timeline named ``name``

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
        Returns current timeline object

        Returns:
            Timeline: timeline object
        """
        from pydavinci.wrappers.timeline import Timeline

        return Timeline(self._obj.GetCurrentTimeline())

    def refresh_luts(self) -> bool:
        """
        Refresh luts

        Returns:
            None: None
        """
        return self._obj.RefreshLUTList()

    def __repr__(self) -> str:
        return f'Project(Name: "{self.name})"'
