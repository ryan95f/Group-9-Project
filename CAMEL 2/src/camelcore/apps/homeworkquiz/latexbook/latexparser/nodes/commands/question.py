from latexbook.latexparser.nodes.command import CommandNode


class Question(CommandNode):
    """Represents the actual question-text."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Question, self).__init__(children=children)
