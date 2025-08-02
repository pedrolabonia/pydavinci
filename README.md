<h1 align='center'>pydavinci</h1>

<p align='center'>A lightly opinionated DaVinci Resolve Python API wrapper</p>

<p align='center'>Provides auto completion, type hints and great API reference documentation.</p>

<p align='center'><sup><i align='center'>I really just wanted auto completion in the IDE and to program transcoding RAW formats</i></sup></p>

---

## Install PyDavinci

- PyDavinci requires Python 3.10 or higher
- External scripting with PyDavinci requires Resolve Studio 18 (Free version does not allow API access)
- There is currently no release version for the Resolve 18 branch. Install it with git.

```bash
pip install git+https://github.com/pedrolabonia/pydavinci@resolve_18
```

Now, with Davinci Resolve open, we just need to import it!

```python
from pydavinci import davinci

resolve = davinci.Resolve()
```

### Examples and documentation

- Check out the usage [examples](https://pedrolabonia.github.io/pydavinci/examples/premiereproxies/)
- Or go deep in the [documentation](https://pedrolabonia.github.io/pydavinci/resolve/)

---

### Installation requirements and guidelines

For launching scripts externally, you also need the __Studio__ version.

If you're working with the built-in Davinci Resolve Python console, you need to install ``pydavinci`` for the Python interpreter that's used by Davinci's console.

For avoiding conflicts when using inside the embedded console, don't use `resolve` as the entry point variable, as that's reserved by the console. Example of suggested usage:

<img src=https://user-images.githubusercontent.com/4316044/164998485-8a4e6fa7-3f8c-436c-b9ab-43350a3e6766.png />

---

### Launching scripts externally (Studio version)


For `pydavinci` to work by launching scripts outside the embedded console, make sure external scripting is set to `Local` in `Settings -> System -> General`

<img src=https://user-images.githubusercontent.com/4316044/164954498-de350d02-0458-478d-a766-6404b7a8a75b.png />

## To-do and contributing

Contributors are always welcome! I currently have a few things I want to change, some of them are:
- [X] ~~Document all possible values of `get_setting` and `set_setting`~~ _New in 0.2.0!_
- [X] ~~Add a better way of interfacing with the whole `get_setting` and `set_setting` methods using a proxy class or something to that effect~~ _New in 0.2.0!_
- [X] ~~Deal with markers in a better way~~ _New in 0.2.0!_
- [ ] Auto launch Resolve when it's not open - I've ran into some issues while trying to connect to the C extension right after launching it, a dirty way to do it is to just implement a `time.sleep` before trying to import the fusionscript module, otherwise we'll need to create another entrypoint to the api for launching the process and then signaling when it's ready 
- [ ] Do the same wrapper made for settings to Metadata and Properties

#### If you want to contribute feel free to open a pull request!

## Documentation
Up to date docs are still a work in progress. At some point expect to see the original API reference extended and some further examples included. For now go to the original [PyDavinci project](https://github.com/pedrolabonia/pydavinci)

Here's a quick list of changes and added API support not present in the [original docs](https://pedrolabonia.github.io/pydavinci/resolve/):

- Python 3.10 typing
- Using [Hatch](https://hatch.pypa.io/latest/) for project management
- Using [Ruff](https://github.com/charliermarsh/ruff) for linting
- Added [Gallery API wrapper](https://github.com/in03/pydavinci/commit/10e7be6b4a4f538c2dec948857a7e3b1af9181a0) (untested)
- Added [timeline.settings.timecode](https://github.com/in03/pydavinci/commit/67bb10f07414df040c511ff781cacd5c1d2eda4c) setter
- Support Resolve's [GetUniqueID](https://github.com/in03/pydavinci/commit/f7520595a3708a0ca2b64a151de014c9b61b7318) method

