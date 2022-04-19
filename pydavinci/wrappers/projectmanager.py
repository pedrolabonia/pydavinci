# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List, Dict
from pydavinci.main import resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers.project import Project


class ProjectManager(object):

    _obj = resolve_obj.GetProjectManager()

    def __init__(self) -> None:
        pass

    @property
    def project(self) -> "Project":
        from pydavinci.wrappers.project import Project

        return Project()

    def create_project(self, project_name: str):
        created = ProjectManager._obj.CreateProject(project_name)
        return Project(created)

    def load_project(self, project_name: str) -> bool:
        return ProjectManager._obj.LoadProject(project_name)

    def create_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.CreateFolder(folder_name)

    def delete_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.DeleteFolder(folder_name)

    def project_list(self) -> List[str]:
        return ProjectManager._obj.GetProjectListInCurrentFolder()

    def folder_list(self) -> List[str]:
        return ProjectManager._obj.GetFolderListInCurrentFolder()

    def goto_root_folder(self) -> bool:
        return ProjectManager._obj.GotoRootFolder()

    def goto_parent_folder(self) -> bool:
        return ProjectManager._obj.GotoParentFolder()

    @property
    def folder(self) -> str:
        return ProjectManager._obj.GetCurrentFolder()

    def open_folder(self, folder_name: str) -> bool:
        return ProjectManager._obj.OpenFolder(folder_name)

    def import_project(self, path: str) -> bool:
        return ProjectManager._obj.ImportProject(path)

    def export_project(self, project_name: str, path: str, stills_and_luts: bool = True) -> bool:
        return ProjectManager._obj.ExportProject(project_name, path, stills_and_luts)

    def restore_project(self, path: str) -> bool:
        return ProjectManager._obj.RestoreProject(path)

    @property
    def db(self) -> dict:
        return ProjectManager._obj.GetCurrentDatabase()

    @db.setter
    def db(self, db_info: dict) -> bool:
        return ProjectManager._obj.SetCurrentDatabase(db_info)

    @property
    def db_list(self) -> List[Dict]:
        return ProjectManager._obj.GetDatabaseList()
