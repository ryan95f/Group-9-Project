from .environment import EnvironmentNode


class ListEnvironmentNode(EnvironmentNode):
    """An abstract node which represents a list environment."""
    def __init__(self, children=None):
        """Initialise the list environment node."""
        super(ListEnvironmentNode, self).__init__(children=children)


class Itemize(ListEnvironmentNode):
    """An unordered list environment."""
    def __init__(self, children=None):
        """Initialise the itemize list environment node."""
        super(Itemize, self).__init__(children=children)


class Enumerate(ListEnvironmentNode):
    """An ordered list environment."""
    def __init__(self, children=None):
        """Initialise the enumerate list environment node."""
        super(Enumerate, self).__init__(children=children)
