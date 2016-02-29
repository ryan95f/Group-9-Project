from latexbook.latexparser.nodes.command import CommandNode

class Item(CommandNode):
    """An item command node."""
    def __init__(self, children=None):
        super(Item, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<li class='latex_command_item'>",
            process_children=True,
            suffix_text="</li>"
        )
