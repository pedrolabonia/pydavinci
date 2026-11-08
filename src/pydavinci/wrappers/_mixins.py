"""Functions shared by [``TimelineItem``][pydavinci.wrappers.timelineitem.TimelineItem] and
[``PhotoAlbumItem``][pydavinci.wrappers.photoalbumitem.PhotoAlbumItem]."""
from typing import TYPE_CHECKING, Any, List, Optional, Union

from pydavinci.utils import as_list, get_resolveobj, get_resolveobjs
from pydavinci.wrappers import constants

if TYPE_CHECKING:
    from pydavinci.wrappers.colorgroup import ColorGroup
    from pydavinci.wrappers.effect import Effect
    from pydavinci.wrappers.graph import Graph

EFFECT_CATEGORIES = ["fusion", "ofx", "audio"]


class FusionCompMixin:
    """Fusion compositions of an item. Compositions are returned as Fusion ``Composition`` objects."""

    _obj: Any

    @property
    def fusion_comp_count(self) -> int:
        """
        Returns the number of Fusion compositions of this item

        Returns:
            int: number of compositions
        """
        return self._obj.GetFusionCompCount()

    @property
    def fusion_comp_names(self) -> List[str]:
        """
        Returns the names of the Fusion compositions of this item

        Returns:
            List[str]: composition names
        """
        return as_list(self._obj.GetFusionCompNameList())

    def get_fusion_comp(self, comp: Union[int, str]) -> Any:
        """
        Gets a Fusion composition by index (``1 <= comp <= fusion_comp_count``) or by name

        Args:
            comp (Union[int, str]): composition index or name

        Returns:
            Fusion composition, ``None`` if not found
        """
        if isinstance(comp, str):
            return self._obj.GetFusionCompByName(comp)
        return self._obj.GetFusionCompByIndex(comp)

    def add_fusion_comp(self) -> Any:
        """
        Adds a new Fusion composition to this item

        Returns:
            new Fusion composition
        """
        return self._obj.AddFusionComp()

    def import_fusion_comp(self, path: str) -> Any:
        """
        Imports a Fusion composition from ``path`` as a new composition of this item

        Args:
            path (str): path to a ``.comp`` file

        Returns:
            imported Fusion composition
        """
        return self._obj.ImportFusionComp(path)

    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        """
        Exports the Fusion composition ``comp_index`` to ``path``

        Args:
            path (str): target file path
            comp_index (int): composition index, starts at ``1``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportFusionComp(path, comp_index)

    def delete_fusion_comp(self, comp_name: str) -> bool:
        """
        Deletes the Fusion composition ``comp_name``

        Args:
            comp_name (str): composition name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteFusionCompByName(comp_name)

    def load_fusion_comp(self, comp_name: str) -> Any:
        """
        Loads the Fusion composition ``comp_name`` as the active composition

        Args:
            comp_name (str): composition name

        Returns:
            loaded Fusion composition
        """
        return self._obj.LoadFusionCompByName(comp_name)

    def rename_fusion_comp(self, old_name: str, new_name: str) -> bool:
        """
        Renames the Fusion composition ``old_name`` to ``new_name``

        Args:
            old_name (str): current composition name
            new_name (str): new composition name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RenameFusionCompByName(old_name, new_name)


class EffectMixin:
    """Effects (``fusion``, ``ofx``, ``audio``) applied to an item."""

    _obj: Any

    def add_effect(self, category: str, effect_id: str) -> Optional["Effect"]:
        """
        Applies an effect to this item

        Args:
            category (str): ``"fusion"``, ``"ofx"`` or ``"audio"``
            effect_id (str): effect id, see ``Resolve.get_effects_list()``

        Returns:
            Optional[Effect]: the applied ``Effect``, ``None`` if it failed
        """
        from pydavinci.wrappers.effect import Effect

        if category not in EFFECT_CATEGORIES:
            raise ValueError(f"Effect category must be one of {EFFECT_CATEGORIES}")
        effect = self._obj.AddEffect(category, effect_id)
        return Effect(effect) if effect else None

    def get_effects(self, category: str) -> List["Effect"]:
        """
        Gets the effects of ``category`` applied to this item

        Args:
            category (str): ``"fusion"``, ``"ofx"`` or ``"audio"``

        Returns:
            List[Effect]: applied effects
        """
        from pydavinci.wrappers.effect import Effect

        if category not in EFFECT_CATEGORIES:
            raise ValueError(f"Effect category must be one of {EFFECT_CATEGORIES}")
        return [Effect(x) for x in as_list(self._obj.GetEffects(category))]

    def delete_effects(self, effects: List["Effect"]) -> bool:
        """
        Removes ``effects`` from this item

        Args:
            effects (List[Effect]): effects to remove

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeleteEffects(get_resolveobjs(effects))


class GradeMixin:
    """Node graph, LUT export, color group and data burn-in of an item."""

    _obj: Any

    def get_node_graph(self, layer_index: Optional[int] = None) -> "Graph":
        """
        Returns the node graph of this item at node stack layer ``layer_index``

        Args:
            layer_index (int, optional): node stack layer, starts at ``1``. Defaults to the first layer.

        Returns:
            Graph: node graph
        """
        from pydavinci.wrappers.graph import Graph

        if layer_index is None:
            return Graph(self._obj.GetNodeGraph())
        return Graph(self._obj.GetNodeGraph(layer_index))

    def reset_all_node_colors(self) -> bool:
        """
        Resets the node color of all nodes in the active version

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ResetAllNodeColors()

    def export_lut(self, export_type: Union[str, float], path: str) -> bool:
        """
        Exports a LUT of the grade to ``path``. Resolve 21.1.2 only exports on the Color page
        (``Resolve.page = "color"``), elsewhere it returns ``False``.

        Args:
            export_type (Union[str, float]): ``"17ptcube"``, ``"33ptcube"``, ``"65ptcube"``, ``"panasonicvlut"``
                or an ``EXPORT_LUT_*`` constant
            path (str): target file path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ExportLUT(constants.lookup("EXPORT_LUT_", export_type), path)

    @property
    def color_group(self) -> Optional["ColorGroup"]:
        """
        Returns the ``ColorGroup`` of this item

        Returns:
            Optional[ColorGroup]: color group, ``None`` if it has none
        """
        from pydavinci.wrappers.colorgroup import ColorGroup

        group = self._obj.GetColorGroup()
        return ColorGroup(group) if group else None

    def assign_to_color_group(self, color_group: "ColorGroup") -> bool:
        """
        Assigns this item to ``color_group``, an existing group of the current project

        Args:
            color_group (ColorGroup): color group

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.AssignToColorGroup(get_resolveobj(color_group))

    def remove_from_color_group(self) -> bool:
        """
        Removes this item from its color group

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.RemoveFromColorGroup()

    def load_burn_in_preset(self, preset_name: str) -> bool:
        """
        Loads the user defined data burn-in preset ``preset_name`` for this item

        Args:
            preset_name (str): preset name

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.LoadBurnInPreset(preset_name)
