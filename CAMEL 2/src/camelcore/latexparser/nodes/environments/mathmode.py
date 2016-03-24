from latexbook.latexparser.nodes.environment import EnvironmentNode


class MathModeNode(EnvironmentNode):
    """An abstract node which represents a mathmode environment."""

    allowed_children = False  # We let MathJax handle this for us! :)

    def __init__(self):
        """Initialise the node."""
        super(MathModeNode, self).__init__()


class Equation(MathModeNode):
    """An equation mathmode environment node."""

    def __init__(self):
        """Initialise the node."""
        super(Equation, self).__init__()


class EqnArray(MathModeNode):
    """An eqnarray mathmode environment node."""

    def __init__(self):
        """Initialise the node."""
        super(EqnArray, self).__init__()


class Cases(MathModeNode):
    """A cases mathmode environment node."""

    def __init__(self):
        """Initialise the node."""
        super(Cases, self).__init__()


class Align(MathModeNode):
    """An align mathmode environment node."""

    def __init__(self):
        """Initialise the node."""
        super(Align, self).__init__()


class Array(MathModeNode):
    """An array mathmode environment node."""

    def __init__(self):
        """Initialise the node."""
        super(Array, self).__init__()
