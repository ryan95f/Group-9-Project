from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.command import CommandNode


class Image(CommandNode):
    """A image command node."""
    def __init__(self, children=None):
        super(Image, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<img class='latex_command_img' />",
            process_children=False,
            suffix_text=None
        )
