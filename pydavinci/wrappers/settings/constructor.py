from typing import TYPE_CHECKING, Any, Dict, Optional, Type, TypeVar

from pydavinci.wrappers.settings.components import (
    Audio,
    Capture,
    Color,
    CommonMonitor,
    CommonSettings,
    Deck,
    Perf,
    Playout,
    ProjectUniqueSettings,
    TimelineMeta,
    TimelineUniqueSettings,
)
from pydavinci.wrappers.settings.map import super_scale_transform

if TYPE_CHECKING:
    from pydavinci.wrappers.project import Project
    from pydavinci.wrappers.settings.validator import BaseConfig
    from pydavinci.wrappers.timeline import Timeline

    AnyModel = TypeVar("AnyModel", bound=BaseConfig)


class _ProjectMeta(ProjectUniqueSettings, CommonMonitor, CommonSettings):
    audio: Audio
    color: Color
    perf: Perf
    deck: Deck
    capture: Capture
    playout: Playout
    timeline: TimelineMeta


class _ProjectSettings(ProjectUniqueSettings, CommonMonitor, CommonSettings):
    pass


class TimelineSettings(TimelineUniqueSettings, TimelineMeta, CommonSettings, CommonMonitor):
    # putting them here so they don't appear first when user calls Timeline.settings
    _selfvalidate: Optional[bool]
    _obj: Optional[Any]


class ProjectSettings(_ProjectMeta, _ProjectSettings):
    # putting them here so they don't appear first when user calls Proejct.settings
    _selfvalidate: Optional[bool]
    _obj: Optional[Any]


def get_appropriate_keys(pydantic_model: Type["AnyModel"], data: Dict[Any, Any]) -> Dict[Any, Any]:

    # Since our base pydantic model is set to not allow extra keys,
    # we need to filter them since from the Davinci API they are all
    # together

    _ret: Dict[str, str] = {}
    data = data
    model = pydantic_model.__fields__
    for value in model.values():
        if value.alias in data.keys():
            _ret[value.alias] = data[value.alias]

    return _ret


def get_prj_settings(obj: "Project") -> ProjectSettings:

    data = obj._obj.GetSetting()

    # First setting validation to off, we just want Pydantic to infer the types for now
    # such as transforming str: "1" into int: 1 or str: "1" to bool: True on a bool field
    data["_selfvalidate"] = False

    audio = Audio.parse_obj(get_appropriate_keys(Audio, data))
    color = Color.parse_obj(get_appropriate_keys(Color, data))
    perf = Perf.parse_obj(get_appropriate_keys(Perf, data))
    deck = Deck.parse_obj(get_appropriate_keys(Deck, data))
    capture = Capture.parse_obj(get_appropriate_keys(Capture, data))
    playout = Playout.parse_obj(get_appropriate_keys(Playout, data))
    timeline = TimelineMeta.parse_obj(get_appropriate_keys(TimelineMeta, data))

    data["superScale"] = super_scale_transform(data["superScale"])

    _projectsettings = _ProjectSettings.parse_obj(
        get_appropriate_keys(_ProjectSettings, data)
    ).dict()

    # From now on we set manually the resolve ._obj so we can call them from the validator
    # later on and avoid sending the settings to the wrong Project instance for example.

    # there's probably a better way to do this but I just
    # spent about 12 hrs non stop trying to figure out how
    # to access an instance from a validator(actually I found out about 3 or 4 ways but
    # this one works best)
    # and I'm not ready for the super duper meta programming yet

    audio._obj = obj._obj
    color._obj = obj._obj
    perf._obj = obj._obj
    deck._obj = obj._obj
    capture._obj = obj._obj
    playout._obj = obj._obj
    timeline._obj = obj._obj
    audio._selfvalidate = True
    color._selfvalidate = True
    perf._selfvalidate = True
    deck._selfvalidate = True
    capture._selfvalidate = True
    playout._selfvalidate = True
    timeline._selfvalidate = True

    const = {
        "audio": audio,
        "color": color,
        "perf": perf,
        "deck": deck,
        "capture": capture,
        "playout": playout,
        "timeline": timeline,
        **_projectsettings,
    }

    # We assemble everything and then pass it to the main ProjectSettings class
    # using pydantic's construct so we don't need to infer the types again

    _ret = ProjectSettings.construct(_fields_set=None, **const)
    _ret._obj = obj._obj
    _ret._selfvalidate = True

    return _ret


def get_tl_settings(obj: "Timeline") -> TimelineSettings:

    # Same thing as above, but way easier since we don't need complex
    # nesting like ProjectSettings.color.setting

    data: Dict[Any, Any] = obj.get_setting()  # type: ignore
    data["superScale"] = super_scale_transform(data["superScale"])

    _ret = TimelineSettings(**data)
    _ret._obj = obj._obj
    _ret._selfvalidate = True

    return _ret
