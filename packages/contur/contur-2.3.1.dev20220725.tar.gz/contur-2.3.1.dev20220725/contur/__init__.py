"""\
The Contur package for model interpretation of collider-physics measurements

Importing the Contur package pulls in the following submodules:

* :mod:`contur.config` - Global configuration options
* :mod:`contur.data` - Database and associated functions parsing data/covariance info from Rivet/YODA
* :mod:`contur.factories` - Main worker classes for contur functionality
* :mod:`contur.plot` - Plotting engine and styling
* :mod:`contur.scan` - Utilities for steering/running creation of MC grids
* :mod:`contur.util` - Misc helper functions

One additional submodule can be manually imported

* :mod:`contur.run` - Defines logic used in python executables
"""

from builtins import open
from builtins import range

import contur.config.version
__version__ = contur.config.version.version
