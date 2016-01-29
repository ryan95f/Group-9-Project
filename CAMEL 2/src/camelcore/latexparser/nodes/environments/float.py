from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.environment import EnvironmentNode


class FloatNode(EnvironmentNode):
    """An abstract node which represents a float environment."""
    def __init__(self, children=None):
        """Initialise the float environment node."""
        super(FloatNode, self).__init__(children=children)


class Figure(FloatNode):
    """A figure float environment node."""
    def __init__(self, children=None):
        """Initialise the figure float environment node."""
        super(Figure, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_figure'>",
            process_children=True,
            suffix_text="</div>"
        )


class Subfigure(Figure):
    """A subfigure float environment node."""
    def __init__(self, children=None):
        """Initialise the subfigure float environment node."""
        super(Subfigure, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_subfigure'>",
            process_children=True,
            suffix_text="</div>"
        )


class Table(Figure):
    """A table float environment node."""
    def __init__(self, children=None):
        """Initialise the table float environment node."""
        super(Table, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<table class='latex_environment_table'>",
            process_children=True,
            suffix_text="</table>"
        )


class Subtable(Table):
    """A subtable float environment node."""
    def __init__(self, children=None):
        """Initialise the subtable float environment node."""
        super(Subtable, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<table class='latex_environment_subtable'>",
            process_children=True,
            suffix_text="</table>"
        )
