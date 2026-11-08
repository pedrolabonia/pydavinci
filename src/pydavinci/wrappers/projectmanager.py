from typing import TYPE_CHECKING, Any, Dict, List, Optional

# from pydavinci.wrappers._basewrappers import BaseResolveWrapper
from pydavinci.main import resolve_obj
from pydavinci.wrappers.project import Project

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import CloudSettings, PyRemoteProjectManager

# import fusionscript as dvr_script


class ProjectManager:
    # try:  ## this is for when we do auto-launch
    #     _obj = resolve_obj.GetProjectManager()  # if using this one here, everything fails
    # except AttributeError:
    #     _obj = get_resolve().GetProjectManager()  # if using this here, closing projects fail

    def __init__(self) -> None:

        self._obj: PyRemoteProjectManager = resolve_obj.GetProjectManager()

    def create_project(self, project_name: str, media_location_path: Optional[str] = None) -> Project:
        """
        Creates a project with ``project_name`` and loads it

        Args:
            project_name (str): project name
            media_location_path (str, optional): media location of the project. Defaults to Resolve's default.

        Returns:
            Project: Project
        """
        if media_location_path is None:
            created = self._obj.CreateProject(project_name)
        else:
            created = self._obj.CreateProject(project_name, media_location_path)
        return Project(created)

    def delete_project(self, project_name: str) -> bool:
        """
        Deletes project ``project_name``

        Args:
            project_name (str): project name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteProject(project_name)

    def load_project(self, project_name: str) -> Project:
        """
        Loads project ``project_name``

        Args:
            project_name (str): project name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return Project(self._obj.LoadProject(project_name))

    def close_project(self, project_name: Project) -> bool:
        """
        Closes project ``project_name``

        Args:
            project_name (str): project name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CloseProject(project_name._obj)

    def create_folder(self, folder_name: str) -> bool:
        """
        Creates project manager folder ``folder_name``

        Args:
            folder_name (str): folder name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.CreateFolder(folder_name)

    def delete_folder(self, folder_name: str) -> bool:
        """
        Deletes project manager folder ``folder_name``

        Args:
            folder_name (str): folder name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteFolder(folder_name)

    @property
    def projects(self) -> List[str]:
        """
        Returns a list with project names in current project manager folder

        Returns:
            List[str]: list of project names
        """
        return self._obj.GetProjectListInCurrentFolder()

    @property
    def folders(self) -> List[str]:
        """
        Returns a list with project manager folder names

        Returns:
            List[str]: list of folder names
        """
        return self._obj.GetFolderListInCurrentFolder()

    def goto_root_folder(self) -> bool:
        """
        Goes to root project manager folder

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.GotoRootFolder()

    def goto_parent_folder(self) -> bool:
        """
        Goes to parent of current project manager folder

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.GotoParentFolder()

    @property
    def folder(self) -> str:
        """
        Returns current folder name

        Returns:
            str: folder name
        """
        return self._obj.GetCurrentFolder()

    def open_folder(self, folder_name: str) -> bool:
        """
        Open folder named ``folder_name``

        Args:
            folder_name (str): folder name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.OpenFolder(folder_name)

    def import_project(self, path: str, project_name: Optional[str] = None) -> bool:
        """
        Imports ``.drp`` project located at ``path``

        Args:
            path (str): path to ``.drp`` project
            project_name (str, optional): name of the imported project. Defaults to the name in the file.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if project_name is None:
            return self._obj.ImportProject(path)
        return self._obj.ImportProject(path, project_name)

    def export_project(self, project_name: str, path: str, stills_and_luts: bool = False) -> bool:
        """
        Exports project

        Args:
            project_name (str): project to be exported
            path (str): path to export to
            stills_and_luts (bool, optional): whether to export with Stills and LUTs. Defaults to False.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportProject(project_name, path, stills_and_luts)

    def restore_project(self, path: str, project_name: Optional[str] = None) -> bool:
        """
        Restore project from ``path``

        Args:
            path (str): project path
            project_name (str, optional): name of the restored project. Defaults to the name in the archive.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if project_name is None:
            return self._obj.RestoreProject(path)
        return self._obj.RestoreProject(path, project_name)

    def archive_project(
        self,
        project_name: str,
        path: str,
        source_media: bool = True,
        render_cache: bool = True,
        proxy_media: bool = False,
    ) -> bool:
        """
        Archives project ``project_name`` to ``path`` (``.dra``). Resolve 21.1.2 returned ``False`` for the
        currently open project in tests.

        Args:
            project_name (str): project to archive
            path (str): target path
            source_media (bool, optional): archive the source media. Defaults to ``True``.
            render_cache (bool, optional): archive the render cache. Defaults to ``True``.
            proxy_media (bool, optional): archive the proxy media. Defaults to ``False``.

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ArchiveProject(project_name, path, source_media, render_cache, proxy_media)

    def get_project_last_modified_time(self, project_name: str) -> Optional[int]:
        """
        Returns the last modification time of project ``project_name`` in the current folder

        Info:
            Resolve 21.1.2 returned ``None`` for every project in tests - ``project_attributes`` has the
            ``lastModifiedDate`` as ISO 8601 string.

        Args:
            project_name (str): project name

        Returns:
            Optional[int]: epoch timestamp
        """
        return self._obj.GetProjectLastModifiedTime(project_name)

    @property
    def project_attributes(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the attributes of all projects in the current folder: project name ->
        ``{"lastModifiedDate", "creationDate", "notes", "liveCollaborationMode"}`` (dates in ISO 8601)

        Returns:
            dict: project attributes
        """
        return self._obj.GetProjectAttributesInCurrentFolder()

    def load_cloud_project(self, cloud_settings: "CloudSettings") -> Optional[Project]:
        """
        Loads a cloud project

        Args:
            cloud_settings (dict): ``projectName`` and ``projectMediaPath`` (required), ``syncMode``
                (``CLOUD_SYNC_*`` constant) - only the first load on a system honors all of them

        Returns:
            Optional[Project]: loaded project, ``None`` if not found
        """
        project = self._obj.LoadCloudProject(cloud_settings)
        return Project(project) if project else None

    def create_cloud_project(self, cloud_settings: "CloudSettings") -> Optional[Project]:
        """
        Creates a cloud project

        Args:
            cloud_settings (dict): ``projectName``, ``projectMediaPath`` (required), ``isCollab``, ``syncMode``,
                ``isCameraAccess``

        Returns:
            Optional[Project]: created project, ``None`` if it failed
        """
        project = self._obj.CreateCloudProject(cloud_settings)
        return Project(project) if project else None

    def import_cloud_project(self, path: str, cloud_settings: "CloudSettings") -> bool:
        """
        Imports a cloud project from ``path``

        Args:
            path (str): project file path
            cloud_settings (dict): cloud settings, ``projectMediaPath`` is required

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ImportCloudProject(path, cloud_settings)

    def restore_cloud_project(self, folder_path: str, cloud_settings: "CloudSettings") -> bool:
        """
        Restores a cloud project from ``folder_path``

        Args:
            folder_path (str): backup folder path
            cloud_settings (dict): cloud settings, ``projectMediaPath`` is required

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RestoreCloudProject(folder_path, cloud_settings)

    @property
    def db(self) -> Dict[str, str]:
        """
        Gets or sets current database.
        For setting a Disk DB:
             ```python
             ProjectManager.db = {
             'DbType': 'Disk',
             'DbName': 'Local Database'
             }
             ```
        For setting a PostgresSQL db:
             ```python
             ProjectManager.db = {
             'DbType': 'PostgreSQL',
             'DbName': 'PostgresDB',
             'IpAddress': '127.0.0.1'
             }
             ```

        Args:
             db_info (dict): valid ``db_info`` dict.


        Returns:
             bool: ``True`` if successful, ``False`` otherwise

        """
        return self._obj.GetCurrentDatabase()

    @db.setter
    def db(self, db_info: Dict[str, str]) -> bool:
        """
        Sets current database according to ``db_info``

         Args:
             db_info (dict): valid ``db_info`` dict.

         Info:
             Valid dictionary:
             ```python
             ProjectManager.db = {
             'DbType': 'Disk',
             'DbName': 'Local Database'
             }
             ```
             For PostgresSQL:
             ```python
             ProjectManager.db = {
             'DbType': 'PostgreSQL',
             'DbName': 'PosgresDB',
             'IpAddress': '127.0.0.1'
             }
             ```

        Returns:
             bool: ``True`` if successful, ``False`` otherwise

        """
        return self._obj.SetCurrentDatabase(db_info)

    @property
    def db_list(self) -> List[Dict[str, str]]:
        """
        Returns list of all databases

        Returns:
            list of databases
        """
        return self._obj.GetDatabaseList()
