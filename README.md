<h1 align='center'>pydavinci</h1>

<p align='center'>A lightly opinionated DaVinci Resolve Python API wrapper</p>

<p align='center'>Provides auto completion, type hints and great API reference documentation.</p>

<p align='center'><sup><i align='center'>I really just wanted auto completion in the IDE and to program transcoding RAW formats</i></sup></p>


---

### Install pydavinci

Install via pip using a __Python 3.6__ environment

```bash
pip install pydavinci

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
pydavinci __only works with `Python 3.6.*`__, as that's a requirement on DaVinci Resolve's part. 

For launching scripts externally, you also need the __Studio__ version.

If you're working with the built-in Davinci Resolve Python console, you need to install ``pydavinci`` for the Python interpreter that's used by Davinci's console.

For avoiding conflicts when using inside the embedded console, don't use `resolve` as the entry point variable, as that's reserved by the console. Example of suggested usage:

<img src=https://user-images.githubusercontent.com/4316044/164998485-8a4e6fa7-3f8c-436c-b9ab-43350a3e6766.png />

---

#### Davinci Resolve v18 beta
For the newer DaVinci Resolve v18, currently in beta, newer Python installations are supported. 

If you want to try out ``pydavinci`` with new Python versions for Resolve v18, use pip with the ``--ignore-requires-python`` flag.

Note that while I did some quick tests, I can't guarantee everything works on Resolve v18 beta. Full testing will become available as further betas come through, and will be supported fully on the official release.

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
