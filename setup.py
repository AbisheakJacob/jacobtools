from setuptools import setup 
from Cython.Build import cythonize

setup(
        ext_modules=cythonize("src/jacobtools/harmonic_mean.pyx")
        )
