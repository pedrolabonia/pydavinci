# pydavinci

A lightly opinionated DaVinci Resolve Python API wrapper

Provides auto completion, type hints and great API reference documentation.

*I really just wanted auto completion in the IDE*


---
pydavinci __requires Python 3.6.*__, as that's a requirements on the software API itself.

For the newer DaVinci Resolve v18, newer Python installations are supported.


## Install pydavinci
```bash
pip install pydavinci

```

Then, use by creating the `Resolve` class:

```python
from pydavinci import davinci

resolve = davinci.Resolve()
```

- Check out the usage [examples](https://pedrolabonia.github.io/pydavinci/examples/premiereproxies/)
- Or go deep in the [documentation](https://pedrolabonia.github.io/pydavinci/resolve/)

---

### To-do and contributing

Contributors are always welcome! I currently have a few things I want to change, some of them are:
- [ ] Document all possible values of `get_setting` and `set_setting`
- [ ] Add a better way of interfacing with the whole `get_setting` and `set_setting` methods using a proxy class or something to that effect
- [ ] Create a Marker class to inherit from for the objects that need it
- [ ] Auto launch Resolve when it's not open - I've ran into some issues while trying to connect to the C extension right after launching it, a dirty way to do it is to just implement a `time.sleep` before trying to import the fusionscript module, otherwise we'll need to create another entrypoint to the api for launching the process and then signaling when it's ready

#### If you want to contribute feel free to open a pull request!
