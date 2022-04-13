from pydavinci import Resolve

if __name__ == "__main__":

    resolve = Resolve()

    project = resolve.project
    project_manager = resolve.project_manager
    media_pool = resolve.media_pool
    media_storage = resolve.media_storage

    print(media_pool._obj)
    print(media_storage)
