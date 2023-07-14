# flake8: noqa
# type: ignore
import random
from cgi import test
from pathlib import Path
from typing import List

import pytest

import pydavinci.wrappers.resolve as davinci
from pydavinci.wrappers.folder import Folder
from pydavinci.wrappers.mediapoolitem import MediaPoolItem
from pydavinci.wrappers.project import Project
from pydavinci.wrappers.settings.constructor import ProjectSettings, TimelineSettings
from pydavinci.wrappers.timeline import Timeline
from pydavinci.wrappers.timelineitem import TimelineItem

# resolve: davinci.Resolve


@pytest.fixture(autouse=True)
def load():
    global resolve
    resolve = davinci.Resolve()
    global settings
    settings = resolve.project.settings


def test_settings_exist():
    assert settings
    assert isinstance(settings, ProjectSettings)


def test_all_initialized():
    assert settings.audio
    assert settings.capture
    assert settings.color
    assert settings.deck
    assert settings.perf
    assert settings.timeline
    assert settings.playout

    assert settings.graphics_white_level


def test_res():
    assert settings.timeline.resolution_height == 1080
    assert settings.timeline.resolution_width == 1920


def test_proxies():
    settings.perf.proxy_media_mode = "disable"
    assert settings.perf.proxy_media_mode == "disable"
    assert resolve.project._obj.GetSetting("perfProxyMediaMode") == "0"

    settings.perf.proxy_media_mode = "prefer_proxies"
    assert settings.perf.proxy_media_mode == "prefer_proxies"
    assert resolve.project._obj.GetSetting("perfProxyMediaMode") == "1"

    settings.perf.proxy_media_mode = "prefer_originals"
    assert settings.perf.proxy_media_mode == "prefer_originals"
    assert resolve.project._obj.GetSetting("perfProxyMediaMode") == "2"


def test_set_res():
    settings.timeline.resolution_height = 500
    assert settings.timeline.resolution_height == 500
    assert resolve.project._obj.GetSetting("timelineResolutionHeight") == "500"


def test_reset_res():
    settings.timeline.resolution_height = 1080
    assert settings.timeline.resolution_height == 1080
    assert resolve.project._obj.GetSetting("timelineResolutionHeight") == "1080"


def test_use_custom_tl_settings():
    tl = resolve.active_timeline
    tl_settings = tl.settings
    assert not tl_settings

    assert tl.custom_settings(True)

    tl_settings = tl.settings
    assert tl_settings


def test_change_tl_settings():
    tl = resolve.active_timeline
    tl_settings = tl.settings
    tl_settings.resolution_height = 777
    assert tl_settings.resolution_height == 777
    assert tl._obj.GetSetting("timelineResolutionHeight") == "777"


def test_assert_settings_are_not_shared():
    tl1 = resolve.active_timeline
    tl1_settings = tl1.settings

    assert resolve.project.open_timeline("Test Timeline 2")

    tl2 = resolve.active_timeline
    assert tl2.name == "Test Timeline 2"
    assert tl2.custom_settings(True)

    tl2_settings = tl2.settings
    assert tl2_settings

    assert tl2_settings.resolution_height != tl1_settings.resolution_height

    tl2_settings.resolution_height = 333
    assert tl2_settings.resolution_height == 333
    assert tl2._obj.GetSetting("timelineResolutionHeight") == "333"
    assert not tl1._obj.GetSetting("timelineResolutionHeight") == "333"


# For some reason the framerate tests below do not work..
# See pydavinci/wrappers/settings/map.py:154 for details

# def test_set_framerate():
#     tl = resolve.active_timeline
#     tl_settings = tl.settings
#     tl_settings.frame_rate = 23.976
#     assert tl_settings.frame_rate == 23.976
#     assert tl._obj.GetSetting("timelineFrameRate") == 23.976


# def test_reset_framerate():
#     tl = resolve.active_timeline
#     tl_settings = resolve.active_timeline.settings
#     tl_settings.frame_rate = 24.0
#     assert tl_settings.frame_rate == 24.0
#     assert tl._obj.GetSetting("timelineFrameRate") == 24.0


def test_reset_custom_settings():
    tl = resolve.active_timeline
    tl_settings = tl.settings
    tl_settings.resolution_height = 1080
    assert tl_settings.resolution_height == 1080
    assert tl._obj.GetSetting("timelineResolutionHeight") == "1080"
    assert tl.custom_settings(False)
    assert tl._obj.GetSetting("useCustomSettings") == "0"

    assert resolve.project.open_timeline("Duplicated")
    tl = resolve.active_timeline
    tl_settings = tl.settings
    tl_settings.resolution_height = 1080
    assert tl_settings.resolution_height == 1080
    assert tl._obj.GetSetting("timelineResolutionHeight") == "1080"
    assert tl.custom_settings(False)
    assert tl._obj.GetSetting("useCustomSettings") == "0"
