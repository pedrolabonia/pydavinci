# flake8: noqa
import time
from typing import List, Optional, TypeVar

import pytest
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem

import pydavinci.wrappers.resolve as davinci
from pydavinci.utils import launch_resolve, process_active
from pydavinci.wrappers.project import Project
from pathlib import Path

import sys

from pydavinci.wrappers.timeline import Timeline

resolve: davinci.Resolve


@pytest.fixture(autouse=True)
def load():

    global resolve
    resolve = davinci.Resolve()


def test_resolve_exists():
    assert resolve._obj is not None


def test_project_manager():
    assert resolve.project_manager is not None


def test_media_storage():
    assert resolve.media_storage is not None


def test_media_pool():
    assert resolve.media_pool is not None


def test_fusion():
    assert resolve.fusion is not None


# TODO: Add layout testing


def test_create_prjmanager_folder():
    assert resolve.project_manager.create_folder("pydavinci_prjmanagerfolder5") is True


def test_open_prjmanager_folder():
    assert resolve.project_manager.open_folder("pydavinci_prjmanagerfolder5") is True


def test_create_and_load_project():
    project = resolve.project_manager.create_project("pydavinci_testproject5")
    assert isinstance(project, Project)


def test_open_project():
    assert isinstance(resolve.project_manager.load_project("pydavinci_testproject5"), Project)


def test_resolve_pages():
    resolve.page = "edit"
    assert resolve.page == "edit"
    resolve.page = "color"
    assert resolve.page == "color"
    resolve.page = "media"
    assert resolve.page == "media"
    resolve.page = "cut"
    assert resolve.page == "cut"
    resolve.page = "fusion"
    assert resolve.page == "fusion"
    resolve.page = "fairlight"
    assert resolve.page == "fairlight"
    resolve.page = "deliver"
    assert resolve.page == "deliver"


## Cleanup for re-running tests


def test_save_project():
    assert resolve.project.save() is True


def test_close_project():
    assert resolve.project.close() is True


def test_delete_prjmanager_folder_and_project():
    assert resolve.project_manager.goto_root_folder() is True
    assert resolve.project_manager.delete_folder("pydavinci_prjmanagerfolder5") is True


def test_mediastorage():
    print(resolve.media_storage.mounted_volumes)
    assert resolve.media_storage.mounted_volumes is not None


def test_create_folder(capsys):
    resolve.page = "media"
    created = resolve.media_pool.add_subfolder(resolve.media_pool.root_folder, "Test Folder")
    assert isinstance(created, Folder)
    assert resolve.media_pool.set_current_folder(created) is True


def test_import_clips_and_import_into_timeline():
    path = Path("./tests/videos")
    imported = resolve.media_pool.import_media(str(path.resolve()))
    assert isinstance(imported, List)
    assert isinstance(imported[0], MediaPoolItem)
    timeline = resolve.media_pool.create_timeline_fromclips("Test Timeline", imported)
    assert isinstance(timeline, Timeline)
    assert timeline.activate() is True


def test_grab_timeline_instance():
    assert isinstance(resolve.active_timeline, Timeline)
