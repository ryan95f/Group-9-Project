"""The various question types that shall be captured from the inputted LaTeX documents."""


from camelcore.latexparser.nodes.environments.list import ListEnvironmentNode


class SingleChoice(ListEnvironmentNode):
    """
    Represents a single choice question.

    For clarification, a single choice must be selected!
    """

    def __init__(self, children=None):
        """Initialise the node."""
        super(SingleChoice, self).__init__(children=children)


class MultipleChoice(ListEnvironmentNode):
    """
    Represents a mutliple choice question.

    For clarification, zero, or more, choices can be selected!
    """

    def __init__(self, children=None):
        """Initialise the node."""
        super(MultipleChoice, self).__init__(children=children)


class MathjaxText(ListEnvironmentNode):
    """Represents a MathJax text input choice."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(MathjaxText, self).__init__(children=children)
