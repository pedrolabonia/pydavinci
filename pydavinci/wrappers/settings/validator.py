from pydantic import BaseModel, validator, Field, PrivateAttr, Extra
from pydavinci.wrappers.settings.map import super_scale_transform
from pydavinci.wrappers.settings.map import SETTINGS_MAP
import pydavinci.logger as log
import pydantic.main


# monkey patch to get underscore fields
def is_valid_field(name: str):
    if not name.startswith("__"):
        return True
    elif name == "__root__":
        return True


pydantic.main.is_valid_field = is_valid_field  # type: ignore


class BaseConfig(BaseModel):
    @validator("*", pre=True)
    def str_none_to_none(cls, value, field):
        # Special case here before everything
        # There are some "None" strings in the data. We want to alter them to the Python None
        # so Pydantic understands it

        if value == "None":
            return None
        return value

    @validator("*")
    def set_prop_validator(cls, v, values, field):

        # This is called on all values assignment

        return resolve_transform(cls, v, values, field)

    class Config:
        extra = "forbid"
        validate_assignment = True
        allow_population_by_field_name = True
        underscore_attrs_are_private = False


def resolve_transform(cls, value, values, field):
    # Here we check if it's superscale, which needs a different transform from/to Resolve
    # we also check if _selfvalidate is False, if it is, it means we're initializing the
    # class and then we just return the value.

    # If _selfvalidate is True, we then see what transform we need to use
    # in the map.py file, which has a dict of the Fields' Aliases to which callable they need to pass through
    # We then pass to the Resolve API the Alias with the right transform function applied

    if field.alias == "superScale":
        return super_scale_transform(value)

    if not values.get("_selfvalidate"):
        log.debug(f"Not sending to Resolve yet. Parsing {field.alias}")

        return value

    if values["_selfvalidate"]:
        log.debug(f"Setting '{field.alias}' to {value}")

        call = SETTINGS_MAP[field.alias]
        values["_obj"].SetSetting(field.alias, call(value))

        return value

    return value
