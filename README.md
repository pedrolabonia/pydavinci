<h1 align='center'>PyDavinci18 🍴</h1>


> **Note**: **This project is a fork of Pydavinci!**
> 
> PyDavinci is developed by [Pedro Labonia](https://github.com/pedrolabonia) 
> - [Original project](https://github.com/pedrolabonia/pydavinci)
> - [Original docs](https://pedrolabonia.github.io/pydavinci)
> - [Original PyPi](https://pypi.org/project/pydavinci/)

---
## Why the fork?
Unfortunately, PyDavinci's progress has slowed, likely due to the pressures and expectations of its developer. I've had plans to publish packages depending on PyDavinci to PyPi, but PyPi doesn't allow publishing packages with git dependencies. Also, Pip allows ignoring required Python versions with the `requires_python` flag, but other package managers or development environments may not place nice. 
### Have you spoken to the dev?

Yes! I am a collaborator on the original project and have shared some thoughts with him on Discord. In fact, Pedro's [resolve_18](https://github.com/pedrolabonia/pydavinci/tree/resolve_18) branch *should* be fairly up-to-date with [main](https://github.com/in03/pydavinci) if I'm doing my job right. All the same, I don't have access to the main repo or the PyPi credentials to push releases and I don't want to be a Karen.

### What can I expect from this fork?
I plan to service my needs here where the official project is lacking, but I'm more than happy to collaborate with others on changes. For the moment I may have a little more free time than Pedro, but I do not plan to supplant him, given he has already demonstrated superior skill and expertise for this project! If in time PyDavinci truly appears abandoned and demand increases, I may take this project in a more headstrong direction. Otherwise, if development picks up again, I will contribute my changes and archive this repository.
 
### Why PyDavinci at all?
I personally think PyDavinci is the most comprehensive and intuitive API wrapper for DaVinci Resolve. I'd like to see it continue growing! It's very thorough and makes building Python apps for Resolve quick and easy.

### Anything else to note?
- Although the package's name is `pydavinci18`, do not install this alongside the original, as installations will collide. The project uses the same namespace as `pydavinci`.
- Documentation is still sparse as I find time to update it! For now go to the original [PyDavinci project](https://github.com/pedrolabonia/pydavinci)

---

## Installation

- PyDavinci requires Python 3.10 or higher
- External scripting with PyDavinci requires Resolve Studio 18 (Free version does not allow API access)

```bash
pip install pydavinci_fork
```

## Usage

```python
# Note: Ensure Davinci Resolve is open before importing

from pydavinci import davinci

resolve = davinci.Resolve()
```

## Documentation
Up to date docs are still a work in progress. At some point expect to see the original API reference extended and some further examples included. 

Here's a quick list of changes and added API support not present in the [original docs](https://pedrolabonia.github.io/pydavinci/resolve/):

- Python 3.10 typing
- Using [Hatch](https://hatch.pypa.io/latest/) for project management
- Using [Ruff](https://github.com/charliermarsh/ruff) for linting
- Added [Gallery API wrapper](https://github.com/in03/pydavinci/commit/10e7be6b4a4f538c2dec948857a7e3b1af9181a0) (untested)
- Added [timeline.settings.timecode](https://github.com/in03/pydavinci/commit/67bb10f07414df040c511ff781cacd5c1d2eda4c) setter
- Support Resolve's [GetUniqueID](https://github.com/in03/pydavinci/commit/f7520595a3708a0ca2b64a151de014c9b61b7318) method
