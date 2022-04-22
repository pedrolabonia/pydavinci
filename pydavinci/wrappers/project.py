from typing import TYPE_CHECKING, Dict, List, Optional

from pydavinci.exceptions import ObjectNotFound
from pydavinci.main import resolve_obj, get_resolve
from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers.mediapool import MediaPool
    from pydavinci.wrappers.timeline import Timeline


class Project(object):
    """Project class.

    Args:
        object (_type_): _description_

    Returns:
        _type_: Object class
    """

    def __init__(self, *args) -> None:
        if args:
            if is_resolve_obj(args[0]):
                self._obj = args[0]
            else:
                raise TypeError(f"{type(args[0])} is not a valid {self.__class__.__name__} type")
        else:
            self._obj = resolve_obj.GetProjectManager().GetCurrentProject()

    @property
    def mediapool(self) -> "MediaPool":
        from pydavinci.wrappers.mediapool import MediaPool

        return MediaPool()

    @property
    def timeline_count(self) -> int:
        return self._obj.GetTimelineCount()

    @property
    def name(self):
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> bool:
        return self._obj.SetName(name)

    @property
    def presets(self) -> list:
        return self._obj.GetPresetList()

    def set_preset(self, preset_name: str) -> bool:
        return self._obj.SetPreset(preset_name)

    def add_renderjob(self) -> str:
        """Adds current render settings to a render job

        Returns:
            str: returns render job id
        """
        return self._obj.AddRenderJob()

    def delete_renderjob(self, job_id: str) -> bool:
        """Deltes render job

        Args:
            job_id (str): render job ID

        Returns:
            bool: True if ID exists, false otherwise
        """
        return self._obj.DeleteRenderJob(job_id)

    def delete_all_renderjobs(self) -> bool:
        """Deletes all renderjobs

        Returns:
            bool: True if succesfull, false otherwise
        """
        return self._obj.DeleteAllRenderJobs()

    @property
    def render_jobs(self) -> list:
        return self._obj.GetRenderJobList()

    @property
    def render_presets(self) -> list:
        return self._obj.GetRenderPresetList()

    def render(self, job_ids: Optional[List[str]] = None, interactive: bool = False) -> bool:
        if not job_ids:
            return self._obj.StartRendering(isInteractiveMode=interactive)
        else:
            return self._obj.StartRendering(job_ids, isInteractiveMode=interactive)

    def stop_render(self) -> None:
        return self._obj.StopRendering()

    def render_status(self, job_id: str) -> Dict:
        return self._obj.GetRenderJobStatus(job_id)

    @property
    def render_formats(self) -> Dict:
        return self._obj.GetRenderFormats()

    @property
    def render_codecs(self) -> Dict:
        return self._obj.GetRenderCodecs()

    @property
    def current_render_format_and_codec(self) -> Dict:
        return self._obj.GetCurrentRenderFormatAndCodec()

    def set_render_format_and_codec(self, format: str, codec: str) -> bool:
        return self._obj.SetCurrentRenderFormatAndCodec(format, codec)

    @property
    def render_mode(self):
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

    def available_resolutions(self, format: str, codec: str) -> Dict:
        return self._obj.GetRenderResolutions(format, codec)

    @property
    def rendering(self) -> bool:
        return self._obj.IsRenderingInProgress()

    def load_render_preset(self, preset_name: str) -> bool:
        return self._obj.LoadRenderPreset(preset_name)

    def save_render_preset_as(self, preset_name: str) -> bool:
        return self._obj.SaveAsNewRenderPreset(preset_name)

    def set_render_settings(self, render_settings: Dict) -> bool:
        return self._obj.SetRenderSettings(render_settings)

    def get_setting(self, setting: str) -> Dict:
        return self._obj.GetSetting(setting)

    def set_setting(self, setting: str, value: str) -> bool:
        return self._obj.SetSetting(setting, value)

    def save(self) -> bool:

        return resolve_obj.GetProjectManager().SaveProject()

    ## note: after loading the first project, it's impossible
    ## to close a project and go back to the window with only
    ## the project manager showing.
    ## It defaults to a 'Untitled Project', and you can't close it
    def close(self) -> bool:
        return resolve_obj.GetProjectManager().CloseProject(self._obj)

    def open_timeline(self, name: str) -> bool:
        from pydavinci.wrappers.timeline import Timeline

        count = self._obj.GetTimelineCount()
        for i in range(count):
            tl = Timeline(self._obj.GetTimelineByIndex(i + 1))
            if tl.name == name:
                return self._obj.SetCurrentTimeline(tl._obj)

        raise ObjectNotFound("Couldn't find timeline by name.")

    @property
    def timeline(self) -> "Timeline":
        from pydavinci.wrappers.timeline import Timeline

        return Timeline(self._obj.GetCurrentTimeline())

    def refresh_luts(self):
        return self._obj.RefreshLUTList()

    def __repr__(self) -> str:
        return f'Project(Name: "{self.name})"'
