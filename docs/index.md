# pydavinci

A lightly opinionated DaVinci Resolve Python API wrapper

Provides auto completion, type hints and great API reference documentation.

<small>*I really just wanted auto completion in the IDE*</small>


!!! note
    pydavinci __requires Python 3.6__, as that's a requirements on the software API itself.

    For the newer DaVinci Resolve v18, newer Python installations are supported.


Install pydavinci
```bash
pip install pydavinci

```

Then, use by importing it:

```python
from pydavinci import davinci

resolve = davinci.Resolve()
```


- Check out the usage [examples](examples/premiereproxies)
- Or go deep in the [documentation](resolve)
