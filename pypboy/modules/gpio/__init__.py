# pypboy/modules/gpio/__init__.py

import pypboy
from . import control_panel

class Module(pypboy.BaseModule):
    """
    This is the main container for the GPIO module.
    It now uses the default BaseModule initializer.
    """
    label = "GPIO"
    submodules = [control_panel.Module]