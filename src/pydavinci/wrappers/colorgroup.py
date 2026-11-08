from typing import TYPE_CHECKING, List, Optional

from pydavinci.utils import as_list, get_resolveobj, is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemoteColorGroup
    from pydavinci.wrappers.graph import Graph
    from pydavinci.wrappers.photoalbum import PhotoAlbum
    from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem
    from pydavinci.wrappers.timeline import Timeline
    from pydavinci.wrappers.timelineitem import TimelineItem


class ColorGroup:
    """A color group of the project, see ``Project.color_groups``."""

    def __init__(self, obj: "PyRemoteColorGroup") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemoteColorGroup" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def name(self) -> str:
        """
        Gets or sets the color group name

        Returns:
            str: name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> None:
        self._obj.SetName(name)

    def get_clips_in_timeline(self, timeline: Optional["Timeline"] = None) -> List["TimelineItem"]:
        """
        Gets the ``TimelineItem``s of this group in ``timeline``

        Args:
            timeline (Timeline, optional): timeline. Defaults to the current timeline.

        Returns:
            List[TimelineItem]: timeline items of this group
        """
        from pydavinci.wrappers.timelineitem import TimelineItem

        if timeline is None:
            items = self._obj.GetClipsInTimeline()
        else:
            items = self._obj.GetClipsInTimeline(get_resolveobj(timeline))
        return [TimelineItem(x) for x in as_list(items)]

    def get_photos_in_photo_album(
        self, photo_album: Optional["PhotoAlbum"] = None
    ) -> List["PhotoAlbumItem"]:
        """
        Gets the ``PhotoAlbumItem``s of this group in ``photo_album``

        Args:
            photo_album (PhotoAlbum, optional): photo album. Defaults to the current photo album.

        Returns:
            List[PhotoAlbumItem]: photo album items of this group
        """
        from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem

        if photo_album is None:
            items = self._obj.GetPhotosInPhotoAlbum()
        else:
            items = self._obj.GetPhotosInPhotoAlbum(get_resolveobj(photo_album))
        return [PhotoAlbumItem(x) for x in as_list(items)]

    @property
    def pre_clip_node_graph(self) -> "Graph":
        """
        Returns the pre-clip node graph of this group

        Returns:
            Graph: pre-clip graph
        """
        from pydavinci.wrappers.graph import Graph

        return Graph(self._obj.GetPreClipNodeGraph())

    @property
    def post_clip_node_graph(self) -> "Graph":
        """
        Returns the post-clip node graph of this group

        Returns:
            Graph: post-clip graph
        """
        from pydavinci.wrappers.graph import Graph

        return Graph(self._obj.GetPostClipNodeGraph())

    def __repr__(self) -> str:
        return f'ColorGroup(Name: "{self.name}")'
