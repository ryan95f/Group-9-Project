from .command import Command


class Reference(Command):
    """A reference command node."""
    def __init__(self, children=None):
        super(Reference, self).__init__(children=children)


class Citation(Command):
    """A citation command node."""
    def __init__(self, children=None):
        super(Citation, self).__init__(children=children)


class Label(Command):
    """A label command node."""
    def __init__(self, children=None):
        super(Label, self).__init__(children=children)
