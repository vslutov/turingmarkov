# -*- coding: utf-8 -*-

"""Turing machine and markov algorithm emulator.

Algorithm are compiling to python.
Read the doc: <https://github.com/vslutov/turingmarkov>"""

import os
from setuptools import setup, find_packages, Command

setup(name='turingmarkov',
      version='0.1.0',
      description=__doc__,
      maintainer='vslutov',
      maintainer_email='vslutov@yandex.ru',
      url='https://github.com/vslutov/turingmarkov',
      license='WTFPL',
      platforms=['any'],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Console",
                   "Intended Audience :: Education",
                   "Natural Language :: Russian",
                   "Natural Language :: English",
                   "Operating System :: Unix",
                   "Operating System :: Microsoft :: Windows",
                   "Programming Language :: Python :: 3 :: Only",
                   "Topic :: Education",
                   "Topic :: Utilities",
                   "Topic :: Scientific/Engineering"],
      install_requires=['pytest'],
      packages=find_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['turingmarkov = turingmarkov.__main__:main']},
      )
