from latexbook.latexparser.nodes.command import CommandNode


class Image(CommandNode):
    """A image command node."""
    def __init__(self, children=None):
        super(Image, self).__init__(children=children)
