# flake8: noqa
# type: ignore
import random
from pathlib import Path
from typing import List

import pytest

import pydavinci.wrappers.resolve as davinci
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem
from pydavinci.wrappers.project import Project
from pydavinci.wrappers.timeline import Timeline
from pydavinci.wrappers.timelineitem import TimelineItem

# resolve: davinci.Resolve


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


def test_create_folder():
    resolve.page = "media"
    created = resolve.media_pool.add_subfolder("Test Folder", resolve.media_pool.root_folder)
    assert isinstance(created, Folder)
    assert resolve.media_pool.set_current_folder(created) is True


def test_import_clips_and_import_into_timeline():
    path = Path("./tests/videos")
    mp_clips = resolve.media_pool.import_media(str(path.resolve()))
    assert isinstance(mp_clips, List)
    assert isinstance(mp_clips[0], MediaPoolItem)

    resolve.media_pool.set_current_folder(resolve.media_pool.root_folder)
    assert resolve.media_pool.current_folder.name == "Master"
    timeline = resolve.media_pool.create_timeline_from_clips("Test Timeline", mp_clips)

    assert isinstance(timeline, Timeline)
    assert timeline.activate() is True


def test_grab_timeline_instance():
    assert isinstance(resolve.active_timeline, Timeline)


def test_timeline_name():
    assert resolve.active_timeline.name == "Test Timeline"


def test_media_pool_markers(subtests):
    mp_clips = resolve.active_timeline.items("video", 1)

    if len(mp_clips) < 8:
        pytest.fail("Need to use at least 8 clips for the tests to work.")

    for i, clip in enumerate(mp_clips):

        with subtests.test(msg="Loop iteration", i=i):
            rnd = random.randint(1, 30)
            rnd2 = random.randint(1, 5)
            rnd3 = random.randint(1, 45)
            print(f"I: {i} RND1: {rnd} | RND2: {rnd2} | RND3: {rnd3}")
            clip.add_flag("Cyan")
            a = clip.markers.add(
                rnd,
                "Blue",
                f"marker name {i}",
                customdata=f"custom data {rnd3}",
                duration=rnd2,
                note=f"marker note {i}",
            )
            print(a.customdata)
            assert clip.flags[0] == "Cyan"
            marker = clip.markers.find(f"custom data {rnd3}")
            # print([x.customdata for x in clip.markers._cache.values()])
            assert marker is not None
            marker.customdata = f"2custom data {rnd3}"
            marker = clip.markers.find(f"2custom data {rnd3}")
            assert marker is not None
            assert marker.color == "Blue"
            assert marker.duration == rnd2
            assert marker.customdata == f"2custom data {rnd3}"
            assert marker.note == f"marker note {i}"
            assert marker.name == f"marker name {i}"

            assert clip.markers.all[0]._data == {
                "frameid": rnd,
                "color": "Blue",
                "duration": rnd2,
                "note": f"marker note {i}",
                "name": f"marker name {i}",
                "customdata": f"2custom data {rnd3}",
            }
            if i < 3:
                assert clip.markers.delete(frameid=rnd)
            elif i > 6:
                assert clip.markers.delete(color="Blue")
            else:
                assert clip.markers.delete(customdata=f"2custom data {rnd3}")

            assert clip.markers.all == []


def test_grab_mediapoolitems_from_timeline():
    video_track = resolve.active_timeline.items("video", 1)
    for video in video_track:
        assert video.mediapoolitem.flags[0] == "Cyan"


def test_timeline_set_name():
    resolve.active_timeline.name = "Test Timeline 2"
    assert resolve.active_timeline.name == "Test Timeline 2"


def test_get_first_timeline_item():
    resolve.page = "edit"
    assert isinstance(resolve.active_timeline.current_video_item, TimelineItem)


def test_duplicate_and_activate_timeline():
    new_tl = resolve.active_timeline.duplicate_timeline("Duplicated")
    assert isinstance(new_tl, Timeline)
    new_tl.activate()
    assert resolve.active_timeline.name == "Duplicated"
