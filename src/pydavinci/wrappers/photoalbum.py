from typing import TYPE_CHECKING, Any, List, Optional

from pydavinci.utils import as_list, get_resolveobjs, is_resolve_obj

if TYPE_CHECKING:
    from pydavinci.wrappers._resolve_stubs import PyRemotePhotoAlbum
    from pydavinci.wrappers.graph import Graph
    from pydavinci.wrappers.mediapoolitem import MediaPoolItem
    from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem


class PhotoAlbum:
    """A photo album (Photo page, Resolve 21), see ``Project.photo_albums`` and ``MediaPool.create_empty_photo_album``."""

    def __init__(self, obj: "PyRemotePhotoAlbum") -> None:
        if is_resolve_obj(obj):
            self._obj: "PyRemotePhotoAlbum" = obj
        else:
            raise TypeError(f"{type(obj)} is not a valid {self.__class__.__name__} type")

    @property
    def name(self) -> str:
        """
        Gets or sets the photo album name (must be unique)

        Returns:
            str: name
        """
        return self._obj.GetName()

    @name.setter
    def name(self, name: str) -> None:
        self._obj.SetName(name)

    @property
    def id(self) -> str:
        """
        Returns a unique ID for the `PhotoAlbum` item

        Returns:
            str: Unique ID
        """
        return self._obj.GetUniqueId()

    @property
    def photos(self) -> List["PhotoAlbumItem"]:
        """
        Returns the items of this photo album

        Returns:
            List[PhotoAlbumItem]: photo album items
        """
        from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem

        return [PhotoAlbumItem(x) for x in as_list(self._obj.GetPhotoList())]

    @property
    def current_item(self) -> Optional["PhotoAlbumItem"]:
        """
        Returns the current photo album item

        Returns:
            Optional[PhotoAlbumItem]: current item, ``None`` if there is none
        """
        from pydavinci.wrappers.photoalbumitem import PhotoAlbumItem

        item = self._obj.GetCurrentItem()
        return PhotoAlbumItem(item) if item else None

    def delete_photos(self, photos: List["PhotoAlbumItem"]) -> bool:
        """
        Deletes ``photos`` from this photo album

        Args:
            photos (List[PhotoAlbumItem]): items to delete

        Returns:
            bool: ``True`` if successful, ``False`` otherwise
        """
        return self._obj.DeletePhotos(get_resolveobjs(photos))

    @property
    def node_graph(self) -> "Graph":
        """
        Returns the node graph of this photo album

        Returns:
            Graph: node graph
        """
        from pydavinci.wrappers.graph import Graph

        return Graph(self._obj.GetNodeGraph())

    @property
    def mediapoolitem(self) -> Optional["MediaPoolItem"]:
        """
        Returns the ``MediaPoolItem`` of this photo album

        Returns:
            Optional[MediaPoolItem]: media pool item
        """
        from pydavinci.wrappers.mediapoolitem import MediaPoolItem

        item = self._obj.GetMediaPoolItem()
        return MediaPoolItem(item) if item else None

    def grab_still(self) -> Any:
        """
        Grabs a still from the current photo

        Returns:
            Gallery still object
        """
        return self._obj.GrabStill()

    def grab_all_stills(self) -> List[Any]:
        """
        Grabs stills from all photos of the album

        Returns:
            List of gallery still objects
        """
        return as_list(self._obj.GrabAllStills())

    def __repr__(self) -> str:
        return f'PhotoAlbum(Name: "{self.name}")'
