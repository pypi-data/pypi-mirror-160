#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 7/26/22

"""

from setuptools import setup  # must be in top

import numpy

from pathlib import Path
from Cython.Build import cythonize


dir_path = Path(__file__).parent / "smet"

extensions = [str(path) for path in dir_path.glob("**/*.pyx")]

setup(
    ext_modules=cythonize(extensions,
                          compiler_directives={'language_level': "3"}),
    include_dirs=[numpy.get_include()]
)
