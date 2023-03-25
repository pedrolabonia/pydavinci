from typing import TYPE_CHECKING, Any, Optional

from pydavinci.main import resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteResolve
    from pydavinci.wrappers.mediapool import MediaPool
    from pydavinci.wrappers.mediastorage import MediaStorage
    from pydavinci.wrappers.project import Project
    from pydavinci.wrappers.projectmanager import ProjectManager
    from pydavinci.wrappers.timeline import Timeline


class Resolve(object):
    def __init__(self, headless: Optional[bool] = None, path: Optional[str] = None):

        # this check is slow AF, to be implemented when we have auto-launch resolve

        # if not process_active("resolve"):
        #     raise NotImplementedError(
        #         "Couldn't find Davinci Resolve. Please make sure it's running"
        #     )

        self.pages = ["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"]
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

    def import_layout(self, path: str, layout_name: str) -> bool:
        """
        Import ``layout_name`` from ``path``

        Args:
            path (str): path to layout file
            layout_name (str): name to be imported as

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """

        return self._obj.ImportLayoutPreset(path, layout_name)

    def quit(self) -> None:
        """
        Quits Davinci Resolve

        Returns:
            None: None
        """
        return self._obj.Quit()

    def __repr__(self) -> str:
        return f'Resolve(Page: "{self.page}")'
