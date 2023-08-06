#! /usr/bin/env python

try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup


from distutils.log import warn
from glob import glob
from setuptools.dist import Distribution

import os
import sys
import contur
__doc__ = contur.__doc__

from setuptools.command.install import install

data=[]
pre_fold='share/contur'
for maindir,subdir,file_name in os.walk('data'):
    if 'share' in maindir:
      continue
    else:
      for filename in file_name:
          data.append((os.path.join(pre_fold,maindir),[os.path.join(maindir,filename)]))
data.append((pre_fold,['Makefile']))

for maindir,subdir,file_name in os.walk("tests"):
  for filename in file_name:
    data.append((os.path.join(pre_fold,maindir),[os.path.join(maindir,filename)]))



script=["conturenv.sh"]
for i in os.listdir("bin"):
  if i.startswith("contur"):
    script.append(os.path.join("bin",i))
    

setup(name = "contur",
      version = contur.__version__,
      packages=find_packages(),
      package_dir = {"contur" : "contur"},
      package_data={"contur": ["data/build_database.py","run/run_init.py"]},
      include_package_data=True,
      data_files=data,
      scripts = script,
      install_requires = ["numpy", "scipy", "pandas", "configobj", "matplotlib",
                          "tqdm", "pytest", "pyyaml", "pyslha","click","scikit-learn"],
      author = "The Contur Collaboration",
      #author_email = 'andy.buckley@cern.ch',
      description = 'Model interpretation of collider-physics measurements',
      long_description = __doc__,
      long_description_content_type='text/markdown',
      keywords = 'BSM UFO SLHA LHC HEP physics particle',
      classifiers=["Development Status :: 5 - Production/Stable",
                    "Programming Language :: Python :: 3",
                    "Topic :: Scientific/Engineering :: Physics",
                    "Operating System :: MacOS",
                    "Operating System :: POSIX :: Linux",
                    "License :: OSI Approved :: GNU General Public License (GPL)"],
      platforms=['linux','MacOS'],
      license = 'GPL')
