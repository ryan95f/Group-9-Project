from latexbook.latexparser.nodes.node import NodeHTML
from latexbook.latexparser.nodes.levels import LevelNode
from latexbook.latexparser.nodes.environment import EnvironmentNode


class Theorem(EnvironmentNode):
    def __init__(self, children=None):
        super(Theorem, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_theorem'>",
            process_children=True,
            suffix_text="</div>"
        )


class Lemma(Theorem):
    def __init__(self, children=None):
        super(Lemma, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_lemma'>",
            process_children=True,
            suffix_text="</div>"
        )


class Corollary(Theorem):
    def __init__(self, children=None):
        super(Corollary, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_corollary'>",
            process_children=True,
            suffix_text="</div>"
        )


class Definition(Theorem):
    def __init__(self, children=None):
        super(Definition, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_definition'>",
            process_children=True,
            suffix_text="</div>"
        )


class Remark(Theorem):
    def __init__(self, children=None):
        super(Remark, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_remark'>",
            process_children=True,
            suffix_text="</div>"
        )


class Example(Theorem):
    def __init__(self, children=None):
        super(Example, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_example'>",
            process_children=True,
            suffix_text="</div>"
        )


class Exercise(Theorem):
    def __init__(self, children=None):
        super(Exercise, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_environment_exercise'>",
            process_children=True,
            suffix_text="</div>"
        )
