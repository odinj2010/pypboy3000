import pypboy.modules
from . import status 

class Module(pypboy.modules.Module):

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.submodules = [
            status.Module(self)
        ]
        self.switch_submodule(0)

    def handle_resume(self):
        super(Module, self).handle_resume()