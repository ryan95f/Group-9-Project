"""
The homeworkquiz environment commands.

The way we will be structuring our homeworkquiz's LaTeX syntax will be slightly different to what was initialially
proposed (e.g. https://github.com/dimbyd/camel/blob/master/data/tex/MA1234/03_probability.tex).

Here are a few bullet-points to help illustrate our chosen structure:
- Homework will be displayed on its own page.
- The 'Homework' node contains the content for said homework page.
- The 'Quiz' node is a list, representing a single homework quiz.
- The 'QuizQuestion' node represents a single question belonging to its parent quiz.
"""


from latexbook.latexparser.nodes.environment import EnvironmentNode


class Homework(EnvironmentNode):
    """Holds the contents for a homework page."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Homework, self).__init__(children=children)


class Quiz(EnvironmentNode):
    """Holds the contents for a homework page."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Quiz, self).__init__(children=children)


class QuizQuestion(EnvironmentNode):
    """Holds the contents for a homework page."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(QuizQuestion, self).__init__(children=children)
