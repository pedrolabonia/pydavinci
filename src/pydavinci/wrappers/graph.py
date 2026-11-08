from typing import TYPE_CHECKING, List, Optional, Union

from pydavinci.utils import as_list, is_resolve_obj
from pydavinci.wrappers import constants

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteGraph


class Graph:
    """
    Node graph of a ``TimelineItem``, ``Timeline``, ``PhotoAlbum``, ``PhotoAlbumItem`` or the pre-/post-clip
    graph of a ``ColorGroup``. Node indices start at ``1``.

    Info:
        After [``apply_grade_from_drx``][pydavinci.wrappers.graph.Graph.apply_grade_from_drx] this object no longer
        refers to a valid graph - get a new one from its owner (e.g. ``TimelineItem.get_node_graph()``).
    """

    def __init__(self, obj: "PyRemoteGraph") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteGraph" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def num_nodes(self) -> int:
        """
        Returns the number of nodes in the graph

        Returns:
            int: number of nodes
        """
        return self._obj.GetNumNodes()

    def set_lut(self, node_index: int, lut_path: str) -> bool:
        """
        Sets LUT on the node ``node_index``. ``lut_path`` can be absolute or relative to the LUT folders,
        it must be known to Resolve (see ``Project.refresh_luts()``).

        Args:
            node_index (int): node index, ``1 <= node_index <= num_nodes``
            lut_path (str): LUT path

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetLUT(node_index, lut_path)

    def get_lut(self, node_index: int) -> str:
        """
        Gets the relative LUT path of node ``node_index``

        Args:
            node_index (int): node index

        Returns:
            str: LUT path
        """
        return self._obj.GetLUT(node_index)

    def set_node_cache_mode(self, node_index: int, cache_mode: Union[str, float]) -> bool:
        """
        Sets the cache mode of node ``node_index``

        Args:
            node_index (int): node index
            cache_mode (Union[str, float]): ``"auto_enabled"``, ``"disabled"``, ``"enabled"`` or a ``CACHE_*`` constant

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetNodeCacheMode(node_index, constants.lookup("CACHE_", cache_mode))

    def get_node_cache_mode(self, node_index: int) -> int:
        """
        Gets the cache mode of node ``node_index``, one of the ``CACHE_*`` constants

        Args:
            node_index (int): node index

        Returns:
            int: cache mode
        """
        return self._obj.GetNodeCacheMode(node_index)

    def get_node_label(self, node_index: int) -> str:
        """
        Gets the label of node ``node_index``

        Args:
            node_index (int): node index

        Returns:
            str: node label
        """
        return self._obj.GetNodeLabel(node_index)

    def set_node_label(self, node_index: int, label: str) -> bool:
        """
        Sets the label of node ``node_index``

        Args:
            node_index (int): node index
            label (str): new label

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetNodeLabel(node_index, label)

    def get_node_color(self, node_index: int) -> str:
        """
        Gets the color of node ``node_index``

        Args:
            node_index (int): node index

        Returns:
            str: color name, empty if no color is set
        """
        return self._obj.GetNodeColor(node_index)

    def set_node_color(self, node_index: int, color: str) -> bool:
        """
        Sets the color of node ``node_index``, an empty string clears it

        Args:
            node_index (int): node index
            color (str): color name (``"Orange"``, ``"Teal"``, ...) or ``""``

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetNodeColor(node_index, color)

    def get_tools_in_node(self, node_index: int) -> List[str]:
        """
        Gets the tools used in node ``node_index``

        Args:
            node_index (int): node index

        Returns:
            List[str]: tool names
        """
        return as_list(self._obj.GetToolsInNode(node_index))

    def set_node_enabled(self, node_index: int, enabled: bool) -> bool:
        """
        Enables or disables node ``node_index``

        Args:
            node_index (int): node index
            enabled (bool): ``True`` to enable

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.SetNodeEnabled(node_index, enabled)

    def apply_arri_cdl_lut(self) -> bool:
        """
        Applies ARRI CDL and LUT

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ApplyArriCdlLut()

    def apply_grade_from_drx(
        self,
        drx_path: str,
        grade_mode: int,
        apply_to_all_layers: bool = False,
        keyframe_mode: Optional[Union[str, float]] = None,
    ) -> bool:
        """
        Applies the grade of a ``.drx`` still to this graph. Afterwards this ``Graph`` is no longer valid.

        Args:
            drx_path (str): path to a ``.drx`` file
            grade_mode (int): ``0`` - No keyframes, ``1`` - Source Timecode aligned, ``2`` - Start Frames aligned
            apply_to_all_layers (bool, optional): apply to all node stack layers. Defaults to ``False``.
            keyframe_mode (Union[str, float], optional): ``"all"``, ``"color"``, ``"sizing"`` or a
                ``KEYFRAME_MODE_*`` constant. Defaults to Resolve's default (all).

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        if keyframe_mode is None:
            return self._obj.ApplyGradeFromDRX(drx_path, grade_mode, apply_to_all_layers)
        return self._obj.ApplyGradeFromDRX(
            drx_path, grade_mode, apply_to_all_layers, constants.lookup("KEYFRAME_MODE_", keyframe_mode)
        )

    def reset_all_grades(self) -> bool:
        """
        Resets all grades in the graph

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.ResetAllGrades()

    def __repr__(self) -> str:
        return f"Graph(Nodes: {self.num_nodes})"
