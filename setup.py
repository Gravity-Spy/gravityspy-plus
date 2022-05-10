#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Scott Coughlin (2019)
#
# This file is part of the gravityspy_plus python package.
#
# gravityspy_plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gravityspy_plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gravityspy_plus.  If not, see <http://www.gnu.org/licenses/>.

"""Setup the gravityspy_plus package
"""

from __future__ import print_function

import glob
import os.path

from setuptools import (setup, find_packages)

cmdclass = {}

# -- documentation ------------------------------------------------------------

# import sphinx commands
try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    pass
else:
    cmdclass['build_sphinx'] = BuildDoc

# read description
with open('README.md', 'rb') as f:
    longdesc = f.read().decode().strip()

# -- dependencies -------------------------------------------------------------

setup_requires = [
    'setuptools',
    'pytest-runner',
]

# These pretty common requirement are commented out. Various syntax types
# are all used in the example below for specifying specific version of the
# packages that are compatbile with your software.
install_requires = [
    'django >= 4.0.0',
    'psycopg2-binary',
]

tests_require = [
    'pytest'
]

# For documenation
extras_require = {
    'doc': [
        'matplotlib',
        'ipython',
        'sphinx',
        'numpydoc',
        'sphinx_rtd_theme',
        'sphinxcontrib_programoutput',
    ],
}

# ONLY IF WRAPPING C C++ OR FORTRAN
# -- run setup ----------------------------------------------------------------

packagenames = find_packages()

# Executables go in a folder called bin
PACKAGENAME = 'gravityspy_plus'
DISTNAME = 'gravityspy_plus' #'YOUR DISTRIBTUION NAME (I.E. PIP INSTALL DISTNAME)' Generally good to be same as packagename
AUTHOR = 'Scott Coughlin'
AUTHOR_EMAIL = 'scottcoughlin2014@u.northwestern.edu'
LICENSE = 'GPLv3+'
DESCRIPTION = 'This Django App defines the Gravity Spy Subject model'
GITHUBURL = 'https://github.com/CIERA-Northwestern/template.git'

setup(name=DISTNAME,
      provides=[PACKAGENAME],
      version=__version__,
      description=DESCRIPTION,
      long_description=longdesc,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=packagenames,
      include_package_data=True,
      cmdclass=cmdclass,
      url=GITHUBURL,
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require=extras_require,
      python_requires='>3.6, <4',
      use_2to3=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3+)',
      ],
)
