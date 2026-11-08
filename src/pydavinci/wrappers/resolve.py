from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydavinci.main import resolve_obj
from pydavinci.utils import as_list
from pydavinci.wrappers import constants

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import EncryptDCTLOptions, PyRemoteResolve
    from pydavinci.wrappers.gallery import Gallery
    from pydavinci.wrappers.mediapool import MediaPool
    from pydavinci.wrappers.mediastorage import MediaStorage
    from pydavinci.wrappers.project import Project
    from pydavinci.wrappers.projectmanager import ProjectManager
    from pydavinci.wrappers.timeline import Timeline


class Resolve:
    def __init__(self, headless: Optional[bool] = None, path: Optional[str] = None):

        # this check is slow AF, to be implemented when we have auto-launch resolve

        # if not process_active("resolve"):
        #     raise NotImplementedError(
        #         "Couldn't find Davinci Resolve. Please make sure it's running"
        #     )

        self.pages = ["media", "photo", "cut", "edit", "fusion", "color", "fairlight", "deliver"]
        """Available pages to switch to using [``Resolve.page``][pydavinci.wrappers.resolve.Resolve.page]"""
        self._obj: PyRemoteResolve = resolve_obj

    @property
    def project_manager(self) -> "ProjectManager":
        """Returns the
        [``ProjectManager``][pydavinci.wrappers.projectmanager.ProjectManager-attributes] object.

        Returns:
            (ProjectManager): Project Manager object
        """
        from pydavinci.wrappers.projectmanager import ProjectManager

        return ProjectManager()

    @property
    def media_storage(self) -> "MediaStorage":
        """Returns the
        [``MediaStorage``][pydavinci.wrappers.mediastorage.MediaStorage-attributes] object.

        Returns:
            (MediaStorage): Media Storage object
        """
        from pydavinci.wrappers.mediastorage import MediaStorage

        return MediaStorage()

    @property
    def media_pool(self) -> "MediaPool":
        """Returns the
        [``MediaPool``][pydavinci.wrappers.mediapool.MediaPool-attributes] object.
        Returns:
            (MediaPool): Media Storage object
        """
        from pydavinci.wrappers.mediapool import MediaPool

        return MediaPool()

    @property
    def project(self) -> "Project":
        """Returns the current active
        [``Project``][pydavinci.wrappers.project.Project-attributes] object.

        Returns:
            (Project): Project object
        """
        from pydavinci.wrappers.project import Project

        return Project(resolve_obj.GetProjectManager().GetCurrentProject())

    @property
    def active_timeline(self) -> "Timeline":
        """Returns the current active
        [``Timeline``][pydavinci.wrappers.timeline.Timeline-attributes] object.

        Returns:
            (Timeline): Timeline object
        """
        from pydavinci.wrappers.timeline import Timeline

        return Timeline()

    @property
    def page(self) -> str:
        """
        Gets or sets current [``Resolve Page``][pydavinci.wrappers.resolve.Resolve.pages]. Note that certain methods are only available when in the right page.

        Args:
            page (str): valid page

        Returns:
            None: None
        """
        return self._obj.GetCurrentPage()

    @page.setter
    def page(self, page: str) -> None:
        """
        Page Setter test

        Args:
            page (str): valid page

        Returns:
            None: None
        """
        if page in self.pages:
            self._obj.OpenPage(page)
        else:
            validpages = " ".join(map(str, self.pages))
            raise ValueError(f'"{page}" is not a valid page. Available pages are: {validpages}')

    @property
    def product_name(self) -> str:
        """
        Returns:
            str: product name
        """
        return self._obj.GetProductName()

    @property
    def version(self) -> str:
        """
        Returns:
            str: version
        """
        return self._obj.GetVersionString()

    @property
    def fusion(self) -> Any:
        """Returns the Fusion object.

        Fusion Object:
            This is object is the same as the regular Fusion API. You can call ``fusion.__dir__()``
            to see all available methods.

            See [The last Fusion API documentation for more details.](https://documents.blackmagicdesign.com/UserManuals/Fusion8_Scripting_Guide.pdf)
        Returns:
            (Fusion): Fusion object
        """
        return resolve_obj.Fusion()

    def load_layout(self, layout_name: str) -> bool:
        """
        Loads saved layout named ``layout_name``

        Args:
            layout_name (str): layout name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadLayoutPreset(layout_name)

    def update_layout(self, layout_name: str) -> bool:
        """
        Updates current layout to ``layout_name``

        Args:
            layout_name (str): layout to be updated

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.UpdateLayoutPreset(layout_name)

    def save_layout(self, layout_name: str) -> bool:
        """
        Saves current layout as ``layout_name``

        Args:
            layout_name (str): layout name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SaveLayoutPreset(layout_name)

    def import_layout(self, path: str, layout_name: Optional[str] = None) -> bool:
        """
        Import ``layout_name`` from ``path``

        Args:
            path (str): path to layout file
            layout_name (str, optional): name to be imported as. Defaults to the file name.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if layout_name is None:
            return self._obj.ImportLayoutPreset(path)
        return self._obj.ImportLayoutPreset(path, layout_name)

    def export_layout(self, layout_name: str, path: str) -> bool:
        """
        Exports layout ``layout_name`` to ``path``

        Args:
            layout_name (str): layout name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportLayoutPreset(layout_name, path)

    def delete_layout(self, layout_name: str) -> bool:
        """
        Deletes layout ``layout_name``

        Args:
            layout_name (str): layout name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteLayoutPreset(layout_name)

    @property
    def layouts(self) -> List[str]:
        """
        Returns the names of the saved UI layouts

        Returns:
            List[str]: layout names
        """
        return as_list(self._obj.GetLayoutPresetList())

    def quit(self) -> None:
        """
        Quits Davinci Resolve

        Returns:
            None: None
        """
        return self._obj.Quit()

    @property
    def version_fields(self) -> List[Union[int, str]]:
        """
        Returns the version as list ``[major, minor, patch, build, suffix]``, see also ``version``

        Returns:
            list: version fields
        """
        return as_list(self._obj.GetVersion())

    @property
    def is_studio(self) -> bool:
        """
        Returns whether this is DaVinci Resolve Studio

        Returns:
            bool: ``True`` for Studio
        """
        return self._obj.IsStudio()

    @property
    def gallery(self) -> "Gallery":
        """
        Returns the ``Gallery`` of the current project

        Returns:
            Gallery: gallery
        """
        from pydavinci.wrappers.gallery import Gallery

        return Gallery(self._obj.GetGallery())

    def set_high_priority(self, high_priority: bool = True) -> bool:
        """
        Sets the script execution priority to high or normal

        Args:
            high_priority (bool, optional): ``True`` for high priority. Defaults to ``True``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetHighPriority(high_priority)

    def disable_background_tasks(self) -> None:
        """
        Disables all background tasks (e.g. background transcription and audio classification) for the
        current Resolve session

        Returns:
            None: None
        """
        self._obj.DisableBackgroundTasksForCurrentResolveSession()

    def get_effects_list(self, media_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Returns the effects that can be applied to a timeline item (see ``TimelineItem.add_effect``)

        Args:
            media_type (str, optional): ``"video"`` (default), ``"photo"`` or ``"audio"``

        Returns:
            List[dict]: effects with keys ``category``, ``id``, ``name``
        """
        if media_type is None:
            return as_list(self._obj.GetEffectsList())
        return as_list(self._obj.GetEffectsList(media_type))

    @property
    def keyframe_mode(self) -> float:
        """
        Gets or sets the keyframe mode: a ``KEYFRAME_MODE_*`` constant, set also as ``"all"``, ``"color"`` or
        ``"sizing"``

        Returns:
            float: keyframe mode
        """
        return self._obj.GetKeyframeMode()

    @keyframe_mode.setter
    def keyframe_mode(self, mode: Union[str, float]) -> None:
        self._obj.SetKeyframeMode(constants.lookup("KEYFRAME_MODE_", mode))

    @property
    def fairlight_presets(self) -> List[str]:
        """
        Returns the names of the Fairlight presets (see ``Project.apply_fairlight_preset``)

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetFairlightPresets())

    def import_render_preset(self, path: str) -> bool:
        """
        Imports a render preset from ``path`` and selects it

        Args:
            path (str): preset file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ImportRenderPreset(path)

    def export_render_preset(self, preset_name: str, path: str) -> bool:
        """
        Exports render preset ``preset_name`` to ``path``

        Args:
            preset_name (str): preset name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportRenderPreset(preset_name, path)

    @property
    def burn_in_presets(self) -> List[str]:
        """
        Returns the names of the data burn-in presets

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetBurnInPresetList())

    def import_burn_in_preset(self, path: str) -> bool:
        """
        Imports a data burn-in preset from ``path``

        Args:
            path (str): preset file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ImportBurnInPreset(path)

    def export_burn_in_preset(self, preset_name: str, path: str) -> bool:
        """
        Exports data burn-in preset ``preset_name`` to ``path``

        Args:
            preset_name (str): preset name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportBurnInPreset(preset_name, path)

    def delete_burn_in_preset(self, preset_name: str) -> bool:
        """
        Deletes data burn-in preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteBurnInPreset(preset_name)

    @property
    def keyboard_presets(self) -> List[str]:
        """
        Returns the names of the keyboard presets

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetKeyboardPresetList())

    @property
    def keyboard_preset(self) -> str:
        """
        Returns the name of the active keyboard preset

        Returns:
            str: preset name
        """
        return self._obj.GetCurrentKeyboardPreset()

    def load_keyboard_preset(self, preset_name: str) -> bool:
        """
        Activates keyboard preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadKeyboardPreset(preset_name)

    def import_keyboard_preset(self, path: str, preset_name: Optional[str] = None) -> bool:
        """
        Imports a keyboard preset from ``path``

        Args:
            path (str): preset file path
            preset_name (str, optional): preset name. Defaults to the file name.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if preset_name is None:
            return self._obj.ImportKeyboardPreset(path)
        return self._obj.ImportKeyboardPreset(path, preset_name)

    def export_keyboard_preset(self, preset_name: str, path: str) -> bool:
        """
        Exports keyboard preset ``preset_name`` to ``path``

        Args:
            preset_name (str): preset name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportKeyboardPreset(preset_name, path)

    def delete_keyboard_preset(self, preset_name: str) -> bool:
        """
        Deletes keyboard preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteKeyboardPreset(preset_name)

    @property
    def user_preferences_presets(self) -> List[str]:
        """
        Returns the names of the user preferences presets

        Returns:
            List[str]: preset names
        """
        return as_list(self._obj.GetUserPreferencesPresetList())

    def load_user_preferences_preset(self, preset_name: str) -> bool:
        """
        Loads user preferences preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadUserPreferencesPreset(preset_name)

    def save_user_preferences_preset(self, preset_name: str) -> bool:
        """
        Saves the current user preferences as preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SaveUserPreferencesPreset(preset_name)

    def import_user_preferences_preset(self, path: str, preset_name: Optional[str] = None) -> bool:
        """
        Imports a user preferences preset from ``path``

        Args:
            path (str): preset file path
            preset_name (str, optional): preset name. Defaults to the file name.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if preset_name is None:
            return self._obj.ImportUserPreferencesPreset(path)
        return self._obj.ImportUserPreferencesPreset(path, preset_name)

    def export_user_preferences_preset(self, preset_name: str, path: str) -> bool:
        """
        Exports user preferences preset ``preset_name`` to ``path``

        Args:
            preset_name (str): preset name
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportUserPreferencesPreset(preset_name, path)

    def delete_user_preferences_preset(self, preset_name: str) -> bool:
        """
        Deletes user preferences preset ``preset_name``

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteUserPreferencesPreset(preset_name)

    def validate_dctl(self, dctl_source: str) -> Optional[str]:
        """
        Validates DCTL source code

        Args:
            dctl_source (str): DCTL source code

        Returns:
            Optional[str]: ``None`` if valid, the error message otherwise
        """
        return self._obj.ValidateDCTL(dctl_source)

    def encrypt_dctl(self, path: str, options: Optional["EncryptDCTLOptions"] = None) -> bool:
        """
        Encrypts the DCTL at ``path``

        Args:
            path (str): DCTL file path
            options (dict, optional): ``Name`` (output file name), ``Expiry`` (ISO 8601), ``OutputFolder``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if options is None:
            return self._obj.EncryptDCTL(path)
        return self._obj.EncryptDCTL(path, options)

    def __repr__(self) -> str:
        return f'Resolve(Page: "{self.page}")'
