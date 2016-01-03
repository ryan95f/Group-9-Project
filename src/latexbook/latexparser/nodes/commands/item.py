from .command import Command


class Item(Command):
    """An item command node."""
    def __init__(self, children=None):
        super(Item, self).__init__(children=children)
