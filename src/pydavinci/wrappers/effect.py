from typing import TYPE_CHECKING, Any, Dict, Optional

from pydavinci.utils import is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteEffect


class Effect:
    """An effect applied to a ``TimelineItem`` or ``PhotoAlbumItem`` (see ``add_effect`` / ``get_effects``)."""

    def __init__(self, obj: "PyRemoteEffect") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteEffect" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def info(self) -> Optional[Dict[Any, Any]]:
        """
        Returns information about the effect (keys ``"id"``, ``"name"``, ``"category"``)

        Returns:
            Optional[dict]: effect info
        """
        return self._obj.GetInfo()

    @property
    def enabled(self) -> bool:
        """
        Gets or sets whether the effect is enabled

        Returns:
            bool: ``True`` if enabled
        """
        return self._obj.GetIsEnabled()

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._obj.SetIsEnabled(enabled)

    @property
    def fusion_comp(self) -> Any:
        """
        Returns the Fusion composition of this effect

        Returns:
            Fusion composition, ``None`` if it is not a Fusion effect
        """
        return self._obj.GetFusionComp()

    @property
    def index(self) -> Optional[int]:
        """
        Gets or sets the 1-based index of this effect among the effects of its category

        Returns:
            Optional[int]: index, ``None`` if the effect is no longer applied
        """
        return self._obj.GetIndex()

    @index.setter
    def index(self, index: int) -> None:
        self._obj.SetIndex(index)

    def __repr__(self) -> str:
        info = self.info or {}
        return f'Effect(Name: "{info.get("name")}", Category: "{info.get("category")}")'
