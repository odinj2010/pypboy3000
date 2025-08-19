import pypboy.modules
from . import main

class Module(pypboy.modules.Module):

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        # The list of screens available in this module
        self.submodules = [
            main.Module(self)
        ]
        # Load the first screen by default
        self.switch_submodule(0)

    def handle_resume(self):
        super(Module, self).handle_resume()
