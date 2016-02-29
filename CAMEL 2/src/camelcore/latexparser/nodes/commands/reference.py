from latexbook.latexparser.nodes.command import CommandNode


class Reference(CommandNode):
    """A reference command node."""
    def __init__(self, children=None):
        super(Reference, self).__init__(children=children)


class Citation(CommandNode):
    """A citation command node."""
    def __init__(self, children=None):
        super(Citation, self).__init__(children=children)


class Label(CommandNode):
    """A label command node."""
    def __init__(self, children=None):
        super(Label, self).__init__(children=children)
