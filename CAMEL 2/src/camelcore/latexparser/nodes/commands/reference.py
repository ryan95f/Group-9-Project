from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.command import CommandNode


class Reference(CommandNode):
    """A reference command node."""
    def __init__(self, children=None):
        super(Reference, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<span class='latex_command_reference'>",
            process_children=True,
            suffix_text="</span>"
        )


class Citation(CommandNode):
    """A citation command node."""
    def __init__(self, children=None):
        super(Citation, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<span class='latex_command_citation'>",
            process_children=True,
            suffix_text="</span>"
        )


class Label(CommandNode):
    """A label command node."""
    def __init__(self, children=None):
        super(Label, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<span class='latex_command_label'>",
            process_children=True,
            suffix_text="</span>"
        )
