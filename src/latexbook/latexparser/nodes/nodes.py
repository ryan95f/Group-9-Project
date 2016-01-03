from .node import (
    ArgumentNode, Text
)

from .levels import (
    Book, Chapter, Section, Subsection
)

from .environments.box import (
    Proof, Verbatim, Center
)

from .environments.float import (
    Figure, Subfigure, Table, Subtable,
)

from .environments.list import (
    Itemize, Enumerate
)

from .environments.mathmode import (
    Equation, EqnArray, Cases, Align, Array
)

from .environments.theorem import (
    Theorem, Lemma, Corollary, Definition, Remark, Example, Exercise
)

from .commands.content import (
    Image
)

from .commands.reference import (
    Reference, Citation, Label
)

from .commands.textstyles import (
    TextIt, TextBf, Underline, Emph
)

from .commands.item import (
    Item
)


class Nodes(object):
    """Holds together all our nodes classes - providing several functions to navigate through them."""

    def __init__(self):
        self.node_classes = {}
        self.root_node_id = None
        self.text_node_id = None
        self.argument_node_id = None

    def add_class(self, node_class):
        """Adds the given node class to our node list."""
        self.node_classes[node_class.get_id()] = node_class

    def get_class(self, node_id):
        """Returns the node class with the given node ID."""
        return self.node_classes.get(node_id)

    def set_root_node_id(self, node_id):
        """Sets the root node."""
        node = self.get_class(node_id)
        if node is not None:
            self.root_node_id = node_id
        return node

    def set_text_node_id(self, node_id):
        """Sets the node used for plain-text."""
        node = self.get_class(node_id)
        if node is not None:
            self.text_node_id = node_id
        return node

    def set_argument_node_id(self, node_id):
        """Sets the node used for arguments."""
        node = self.get_class(node_id)
        if node is not None:
            self.argument_node_id = node_id
        return node

    def get_by_attr(self, node_attr):
        """Returns all the node classes which contain an attribute with the given name."""
        found_nodes = []
        for node_id, node in self.node_classes.items():
            if hasattr(node, node_attr):
                found_nodes.append(node)
        return found_nodes


def build_default_nodes():
    """Populates an instance of the class Nodes with all the default classes."""
    nodes = Nodes()

    # Add argument node.
    nodes.add_class(ArgumentNode)
    nodes.set_argument_node_id(ArgumentNode.get_id())

    # Add content text node.
    nodes.add_class(Text)
    nodes.set_text_node_id(Text.get_id())

    # Add level nodes.
    nodes.add_class(Book)
    nodes.set_root_node_id(Book.get_id())
    nodes.add_class(Chapter)
    nodes.add_class(Section)
    nodes.add_class(Subsection)

    # Add box environment nodes.
    nodes.add_class(Proof)
    nodes.add_class(Verbatim)
    nodes.add_class(Center)

    # Add float environment nodes.
    nodes.add_class(Figure)
    nodes.add_class(Subfigure)
    nodes.add_class(Table)
    nodes.add_class(Subtable)

    # Add list environment nodes.
    nodes.add_class(Itemize)
    nodes.add_class(Enumerate)

    # Add mathmode environment nodes.
    nodes.add_class(Equation)
    nodes.add_class(EqnArray)
    nodes.add_class(Cases)
    nodes.add_class(Align)
    nodes.add_class(Array)

    # Add theorem environment nodes.
    nodes.add_class(Theorem)
    nodes.add_class(Lemma)
    nodes.add_class(Corollary)
    nodes.add_class(Definition)
    nodes.add_class(Remark)
    nodes.add_class(Example)
    nodes.add_class(Exercise)

    # Add content command nodes.
    nodes.add_class(Image)

    # Add list command nodes.
    nodes.add_class(Item)

    # Add reference command nodes.
    nodes.add_class(Reference)
    nodes.add_class(Citation)
    nodes.add_class(Label)

    # Add text style command nodes.
    nodes.add_class(TextIt)
    nodes.add_class(TextBf)
    nodes.add_class(Underline)
    nodes.add_class(Emph)

    return nodes
