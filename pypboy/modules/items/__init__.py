import pypboy.modules
from . import weapons
from . import apparel
from . import aid
from . import misc
from . import ammo

class Module(pypboy.modules.Module):

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.submodules = [
            weapons.Module(self),
            apparel.Module(self),
            aid.Module(self),
            misc.Module(self),
            ammo.Module(self)
        ]
        self.switch_submodule(0)

    def handle_resume(self):
        self.pypboy.header.headline = "ITEMS"
        self.pypboy.header.title = ["WEAPONS", "APPAREL", "AID", "MISC", "AMMO"]
        super(Module, self).handle_resume()