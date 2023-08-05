from pymote3 import release

__author__ = '%s <%s>' % release.authors['Arbula']
__license__ = release.license
__version__ = release.version

# For interactive sessions these import names with from pymote3 import *
import os
os.environ['QT_API'] = 'PySide6'
from pymote3.conf import settings
from pymote3.network import Network
from pymote3.networkgenerator import NetworkGenerator
from pymote3.simulation import Simulation
from pymote3.sensor import CompositeSensor
from pymote3.node import Node
from pymote3.environment import Environment
from pymote3.npickle import *
from pymote3.utils.localization import *


# Declare namespace package
from pkgutil import extend_path  #@Reimport
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment
