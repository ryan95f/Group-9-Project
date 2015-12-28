from .command import Command


class Image(Command):
    """A image command node."""
    def __init__(self, children=None):
        super(Image, self).__init__(children=children)
