from typing import TYPE_CHECKING, Dict, List, Optional

from pydavinci.wrappers.project import Project
from pydavinci.wrappers._basewrappers import BaseResolveWrapper
from pydavinci.main import get_resolve, resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers.project import Project

# import fusionscript as dvr_script


class ProjectManager(BaseResolveWrapper):
    # try:
    #     _obj = resolve_obj.GetProjectManager()  # if using this one here, everything fails
    # except AttributeError:
    #     _obj = get_resolve().GetProjectManager()  # if using this here, closing projects fail

    def __init__(self) -> None:

        self._obj = resolve_obj.GetProjectManager()

    def create_project(self, project_name: str) -> "Project":
        created = self._obj.CreateProject(project_name)
        return Project(created)

    def delete_project(self, project_name: str) -> bool:
        return self._obj.DeleteProject(project_name)

    def load_project(self, project_name: str) -> "Project":
        return Project(self._obj.LoadProject(project_name))

    def close_project(self, project: "Project") -> bool:
        return self._obj.CloseProject(project)

    def create_folder(self, folder_name: str):
        return self._obj.CreateFolder(folder_name)

    def delete_folder(self, folder_name: str) -> bool:
        return self._obj.DeleteFolder(folder_name)

    def project_list(self) -> List[str]:
        return self._obj.GetProjectListInCurrentFolder()

    def folder_list(self) -> List[str]:
        return self._obj.GetFolderListInCurrentFolder()

    def goto_root_folder(self) -> bool:
        return self._obj.GotoRootFolder()

    def goto_parent_folder(self) -> bool:
        return self._obj.GotoParentFolder()

    @property
    def folder(self) -> str:
        return self._obj.GetCurrentFolder()

    def open_folder(self, folder_name: str) -> bool:
        print("entru open folder")
        return self._obj.OpenFolder(folder_name)

    def import_project(self, path: str) -> bool:
        return self._obj.ImportProject(path)

    def export_project(self, project_name: str, path: str, stills_and_luts: bool = True) -> bool:
        return self._obj.ExportProject(project_name, path, stills_and_luts)

    def restore_project(self, path: str) -> bool:
        return self._obj.RestoreProject(path)

    @property
    def db(self) -> dict:
        return self._obj.GetCurrentDatabase()

    @db.setter
    def db(self, db_info: dict) -> bool:
        return self._obj.SetCurrentDatabase(db_info)

    @property
    def db_list(self) -> List[Dict]:
        return self._obj.GetDatabaseList()
