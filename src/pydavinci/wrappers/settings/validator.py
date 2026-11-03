from typing import Any, Callable, Optional, Union

from pydantic import BaseModel, ConfigDict, PrivateAttr, field_validator

import pydavinci.logger as log
from pydavinci.wrappers.settings.map import (
    SETTINGS_MAP,
    perf_proxy_media_transform,
    super_scale_transform,
)

_ANY = Optional[Union[str, int, bool]]


class BaseConfig(BaseModel):  # type: ignore
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    # Private attributes, set after initialization (see constructor.py):
    # _obj is the Resolve object the settings belong to and _selfvalidate
    # tells if an assignment should be sent to Resolve
    _selfvalidate: bool = PrivateAttr(default=False)
    _obj: Optional[Any] = PrivateAttr(default=None)

    @field_validator("*", mode="before")
    @classmethod
    def str_none_to_none(cls, value: _ANY) -> _ANY:
        # Special case here before everything
        # There are some "None" strings in the data. We want to alter them to the Python None
        # so Pydantic understands it
        log.debug(f"pre root validator called = {value}")
        if value == "None" or value == "":
            return None
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        # validate_assignment validates the value first and raises on invalid values,
        # so only valid values are sent to Resolve
        super().__setattr__(name, value)
        if name in type(self).model_fields and self._selfvalidate:
            self.__dict__[name] = resolve_transform(self, name, self.__dict__[name])


def resolve_transform(model: BaseConfig, name: str, value: _ANY) -> _ANY:
    # Here we check if it's superscale, which needs a different transform from/to Resolve.
    # This is only called on assignments after initialization (_selfvalidate is True).

    # We then see what transform we need to use in the map.py file, which has a dict of the
    # Fields' Aliases to which callable they need to pass through
    # We then pass to the Resolve API the Alias with the right transform function applied
    log.debug("resolve_transform called")

    alias = type(model).model_fields[name].alias or name

    if alias == "superScale":
        value = super_scale_transform(value)  # type: ignore

    if alias == "perfProxyMediaMode":
        value = perf_proxy_media_transform(value)  # type: ignore

    log.debug(f"Setting '{alias}' to {value}")
    call: Callable[[_ANY], _ANY] = SETTINGS_MAP[alias]  # type: ignore
    model._obj.SetSetting(alias, call(value))  # type: ignore
    return value
