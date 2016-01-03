from .environment import EnvironmentNode


class BoxNode(EnvironmentNode):
    """An abstract node which represents a box environment."""
    def __init__(self, children=None):
        """Initialise the box environment node."""
        super(EnvironmentNode, self).__init__(children=children)


class Proof(BoxNode):
    """A proof box environment node."""
    def __init__(self, children=None):
        """Initialise the proof box environment node."""
        super(Proof, self).__init__(children=children)


class Verbatim(BoxNode):
    """A verbatim box environment node."""

    allowed_children = False  # Don't parse Verbatim contents.

    def __init__(self, children=None):
        """Initialise the verbatim box environment node."""
        super(Verbatim, self).__init__(children=children)


class Center(BoxNode):
    """A center box environment node."""
    def __init__(self, children=None):
        """Initialise the center box environment node."""
        super(Center, self).__init__(children=children)
