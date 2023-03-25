from typing import TYPE_CHECKING, Callable, Dict, Optional, Union

import pydantic.main
from pydantic import BaseModel, validator

import pydavinci.logger as log
from pydavinci.wrappers.settings.map import SETTINGS_MAP, super_scale_transform

if TYPE_CHECKING:
    from pydantic.fields import ModelField


# monkey patch to get underscore fields
def is_valid_field(name: str) -> Optional[bool]:
    if not name.startswith("__"):
        return True
    elif name == "__root__":
        return True
    return None


pydantic.main.is_valid_field = is_valid_field  # type: ignore

_ANY = Optional[Union[str, int, bool]]


class BaseConfig(BaseModel):  # type: ignore
    @validator("*", pre=True)  # type: ignore
    def str_none_to_none(cls: "BaseModel", value: _ANY) -> _ANY:  # noqa: B902
        # Special case here before everything
        # There are some "None" strings in the data. We want to alter them to the Python None
        # so Pydantic understands it
        if value == "None" or value == "":
            return None
        return value

    @validator("*")  # type: ignore
    def set_prop_validator(
        cls: "BaseModel", v: _ANY, values: Dict[_ANY, _ANY], field: "ModelField"  # noqa: B902
    ) -> _ANY:

        # This is called on all values assignment

        return resolve_transform(cls, v, values, field)

    class Config:
        extra = "forbid"
        validate_assignment = True
        allow_population_by_field_name = True
        underscore_attrs_are_private = False


def resolve_transform(
    cls: "BaseModel", value: _ANY, values: Dict[_ANY, _ANY], field: "ModelField"
) -> _ANY:
    # Here we check if it's superscale, which needs a different transform from/to Resolve
    # we also check if _selfvalidate is False, if it is, it means we're initializing the
    # class and then we just return the value.

    # If _selfvalidate is True, we then see what transform we need to use
    # in the map.py file, which has a dict of the Fields' Aliases to which callable they need to pass through
    # We then pass to the Resolve API the Alias with the right transform function applied

    if field.alias == "superScale":
        return super_scale_transform(value)  # type: ignore

    if not values.get("_selfvalidate"):
        log.debug(f"Not sending to Resolve yet. Parsing {field.alias}")

        return value

    if values["_selfvalidate"]:
        log.debug(f"Setting '{field.alias}' to {value}")

        call: Callable[[_ANY], _ANY] = SETTINGS_MAP[field.alias]  # type: ignore
        values["_obj"].SetSetting(field.alias, call(value))  # type: ignore

        return value

    return value
