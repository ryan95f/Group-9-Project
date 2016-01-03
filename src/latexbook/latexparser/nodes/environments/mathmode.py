from .environment import EnvironmentNode


class MathModeNode(EnvironmentNode):
    allowed_children = False  # We let MathJax handle this for us! :)

    """An abstract node which represents a mathmode environment."""
    def __init__(self):
        """Initialise the mathmode environment node."""
        super(MathModeNode, self).__init__()


class Equation(MathModeNode):
    """An equation mathmode environment node."""
    def __init__(self):
        """Initialise the equation mathmode environment node."""
        super(Equation, self).__init__()


class EqnArray(MathModeNode):
    """An eqnarray mathmode environment node."""
    def __init__(self):
        """Initialise the eqnarray mathmode environment node."""
        super(EqnArray, self).__init__()


class Cases(MathModeNode):
    """An cases mathmode environment node."""
    def __init__(self):
        """Initialise the cases mathmode environment node."""
        super(Cases, self).__init__()


class Align(MathModeNode):
    """An align mathmode environment node."""
    def __init__(self):
        """Initialise the align mathmode environment node."""
        super(Align, self).__init__()


class Array(MathModeNode):
    """An array mathmode environment node."""
    def __init__(self):
        """Initialise the array mathmode environment node."""
        super(Array, self).__init__()
