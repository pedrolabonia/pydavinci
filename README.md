# pydavinci

A lightly opinionated DaVinci Resolve Python API wrapper

Provides auto completion, type hints and great API reference documentation.

<small>*I really just wanted auto completion in the IDE*</small>


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

---

- Check out the usage [examples](https://pedrolabonia.github.io/pydavinci/examples/premiereproxies/)
- Or go deep in the [documentation](https://pedrolabonia.github.io/pydavinci/resolve/)
