from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.environment import EnvironmentNode


class MathModeNode(EnvironmentNode):
    allowed_children = False  # We let MathJax handle this for us! :)

    """An abstract node which represents a mathmode environment."""
    def __init__(self):
        """Initialise the mathmode environment node."""
        super(MathModeNode, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_mathmode'>",
            process_children=True,
            suffix_text="</div>"
        )


class Equation(MathModeNode):
    """An equation mathmode environment node."""
    def __init__(self):
        """Initialise the equation mathmode environment node."""
        super(Equation, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_equation'>",
            process_children=True,
            suffix_text="</div>"
        )


class EqnArray(MathModeNode):
    """An eqnarray mathmode environment node."""
    def __init__(self):
        """Initialise the eqnarray mathmode environment node."""
        super(EqnArray, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_eqnarray'>",
            process_children=True,
            suffix_text="</div>"
        )

class Cases(MathModeNode):
    """An cases mathmode environment node."""
    def __init__(self):
        """Initialise the cases mathmode environment node."""
        super(Cases, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_cases'>",
            process_children=True,
            suffix_text="</div>"
        )

class Align(MathModeNode):
    """An align mathmode environment node."""
    def __init__(self):
        """Initialise the align mathmode environment node."""
        super(Align, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_align'>",
            process_children=True,
            suffix_text="</div>"
        )

class Array(MathModeNode):
    """An array mathmode environment node."""
    def __init__(self):
        """Initialise the array mathmode environment node."""
        super(Array, self).__init__()

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_array'>",
            process_children=True,
            suffix_text="</div>"
        )
