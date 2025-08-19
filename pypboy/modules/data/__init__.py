import pypboy.modules
# Import the data submodules here when they are created
# from . import quests, misc, radio

class Module(pypboy.modules.Module):

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self.submodules = [
            # quests.Module(self),
            # misc.Module(self),
            # radio.Module(self)
        ]
        # For now, it's empty. We will add submodules later.
        print("DATA Module initialized")

    def handle_resume(self):
        self.pypboy.header.headline = "DATA"
        # self.pypboy.header.title = ["QUESTS", "MISC", "RADIO"]
        super(Module, self).handle_resume()