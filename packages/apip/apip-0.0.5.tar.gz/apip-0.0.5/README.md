# apip
[![Built with Python](https://img.shields.io/badge/-Python-3c679c?style=for-the-badge&logo=Python&logoColor=fae583)](https://python.org)
[![Built with Aiohttp](https://img.shields.io/badge/-Aiohttp-FFFFFF?style=for-the-badge&logo=Aiohttp&logoColor=blue)](https://docs.aiohttp.org/en/stable/)

---
An easy, high level wrapper for the Pip API. It uses `subprocess` to
use the Pip CLI and wrap it into an easier to use package in Python.
---

## Installation
**Requires Python 3.7+**

To install `apip` on PyPi, run 
```shell
pip install apip
```
---

## API Coverage
This table covers the coverage of apip

| Feature             | Supported                                                                                                |
|---------------------|----------------------------------------------------------------------------------------------------------|
| Installing Packages | <img alt="✅" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/2705.png" width=15>   |
| Error Porting       | <img alt="✅" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/2705.png" width=15>   |
| Pypi API | <img alt="⚠️" src="https://somehybrid.github.io/cdn/warning.png" width=15>*                              |
| Getting individual version packages | <img alt="🚫" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/1f6ab.png" width=15> |

<img alt="⚠️" src="https://somehybrid.github.io/cdn/warning.png" width=15>: This feature does not have full coverage yet.

## Quickstart
To get started and see what `apip` can do, run some example programs.
```python
>>> import apip
>>> pip = apip.Pip()
>>> pip.get("module")
>>> print(pip.list())
```