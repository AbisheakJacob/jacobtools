# DOCUMENTATION

## Build

Delete **dist** folder in the root directory.

```powershell
python -m build
```

## Local Installation

In the root directory, run the below command:

```powershell
py -m pip install .
```

## Integrating Cython

1. Update the **requires** values in the **build-system** section of pyproject.toml to include "**cython**"
2. Python files marked for Cython conversion to C should have a extension of *.pyx*
3. Create **setup.py** file in the root folder, the sample contents of the **setup.py** file is given below

```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("src/jacobtools/harmonic_mean.pyx")
)
```
- Most python packages such as numpy, pandas etc are written using C base, hence a cython wrapper on top will not increase performance
- Cython is useful when used for heavy numerical computation and huge loops.
