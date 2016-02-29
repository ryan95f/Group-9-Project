from latexbook.latexparser.nodes.environment import EnvironmentNode


class Theorem(EnvironmentNode):
    def __init__(self, children=None):
        super(Theorem, self).__init__(children=children)


class Lemma(Theorem):
    def __init__(self, children=None):
        super(Lemma, self).__init__(children=children)

class Corollary(Theorem):
    def __init__(self, children=None):
        super(Corollary, self).__init__(children=children)


class Definition(Theorem):
    def __init__(self, children=None):
        super(Definition, self).__init__(children=children)


class Remark(Theorem):
    def __init__(self, children=None):
        super(Remark, self).__init__(children=children)


class Example(Theorem):
    def __init__(self, children=None):
        super(Example, self).__init__(children=children)


class Exercise(Theorem):
    def __init__(self, children=None):
        super(Exercise, self).__init__(children=children)
