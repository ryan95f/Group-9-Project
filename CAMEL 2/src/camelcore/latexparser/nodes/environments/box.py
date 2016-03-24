from latexbook.latexparser.nodes.environment import EnvironmentNode


class BoxNode(EnvironmentNode):
    """An abstract node which represents a box environment."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(EnvironmentNode, self).__init__(children=children)


class Proof(BoxNode):
    """A proof box environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Proof, self).__init__(children=children)


class Verbatim(BoxNode):
    """A verbatim box environment node."""

    allowed_children = False  # Don't parse Verbatim contents.

    def __init__(self, children=None):
        """Initialise the node."""
        super(Verbatim, self).__init__(children=children)


class Center(BoxNode):
    """A center box environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Center, self).__init__(children=children)
