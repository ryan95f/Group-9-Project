from latexbook.latexparser.nodes.environment import EnvironmentNode


class FloatNode(EnvironmentNode):
    """An abstract node which represents a float environment."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(FloatNode, self).__init__(children=children)


class Figure(FloatNode):
    """A figure float environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Figure, self).__init__(children=children)


class Subfigure(Figure):
    """A subfigure float environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Subfigure, self).__init__(children=children)


class Table(Figure):
    """A table float environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Table, self).__init__(children=children)


class Subtable(Table):
    """A subtable float environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Subtable, self).__init__(children=children)
