from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.environment import EnvironmentNode


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

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<ul class='latex_environment_itemize'>",
            process_children=True,
            suffix_text="</ul>"
        )


class Enumerate(ListEnvironmentNode):
    """An ordered list environment."""
    def __init__(self, children=None):
        """Initialise the enumerate list environment node."""
        super(Enumerate, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<ol class='latex_environment_enumerate'>",
            process_children=True,
            suffix_text="</ol>"
        )
