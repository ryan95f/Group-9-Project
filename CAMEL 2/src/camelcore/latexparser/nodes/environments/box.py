from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.environment import EnvironmentNode


class BoxNode(EnvironmentNode):
    """An abstract node which represents a box environment."""
    def __init__(self, children=None):
        """Initialise the box environment node."""
        super(EnvironmentNode, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_theorem'>",
            process_children=True,
            suffix_text="</div>"
        )


class Proof(BoxNode):
    """A proof box environment node."""
    def __init__(self, children=None):
        """Initialise the proof box environment node."""
        super(Proof, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_proof'>",
            process_children=True,
            suffix_text="</div>"
        )


class Verbatim(BoxNode):
    """A verbatim box environment node."""

    allowed_children = False  # Don't parse Verbatim contents.

    def __init__(self, children=None):
        """Initialise the verbatim box environment node."""
        super(Verbatim, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_verbatim'>",
            process_children=False,
            suffix_text="</div>"
        )


class Center(BoxNode):
    """A center box environment node."""
    def __init__(self, children=None):
        """Initialise the center box environment node."""
        super(Center, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_center'>",
            process_children=True,
            suffix_text="</div>"
        )
