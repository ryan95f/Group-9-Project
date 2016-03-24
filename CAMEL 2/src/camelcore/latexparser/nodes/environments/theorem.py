from latexbook.latexparser.nodes.environment import EnvironmentNode


class Theorem(EnvironmentNode):
    """A theorem environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Theorem, self).__init__(children=children)


class Lemma(EnvironmentNode):
    """A lemma environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Lemma, self).__init__(children=children)


class Corollary(EnvironmentNode):
    """A corollary environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Corollary, self).__init__(children=children)


class Definition(EnvironmentNode):
    """A definition environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Definition, self).__init__(children=children)


class Remark(EnvironmentNode):
    """A remark environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Remark, self).__init__(children=children)


class Example(EnvironmentNode):
    """An example environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Example, self).__init__(children=children)


class Exercise(EnvironmentNode):
    """An exercise environment node."""

    def __init__(self, children=None):
        """Initialise the node."""
        super(Exercise, self).__init__(children=children)
