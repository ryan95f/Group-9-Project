"""
	Defines a configuration of NodeBank that we can use to test the functionality of our LaTeX parser.
"""

# Import our 'Nodes' class.
from ...nodebank import (
    NodeBank
)

# Import all the nodes that we want the parser to utilise.
from ...nodes.node import (
    ArgumentNode, TextNode
)

from ...nodes.levels import (
    Book, Chapter, Section, Subsection
)

from .nodes.environments import (
    Proof, Verbatim,
)

from .nodes.commands import (
    TextIt, Emph
)

BOOKNODES = NodeBank()

# Add argument node.
BOOKNODES.add_class(ArgumentNode)
BOOKNODES.set_argument_node_id(ArgumentNode.get_id())

# Add content text node.
BOOKNODES.add_class(TextNode)
BOOKNODES.set_text_node_id(TextNode.get_id())

# Add level nodes.
BOOKNODES.add_class(Book)
BOOKNODES.set_root_node_id(Book.get_id())
BOOKNODES.add_class(Chapter)
BOOKNODES.add_class(Section)
BOOKNODES.add_class(Subsection)

# Add box environment nodes.
BOOKNODES.add_class(Proof)
BOOKNODES.add_class(Verbatim)

# Add text style command nodes.
BOOKNODES.add_class(TextIt)
BOOKNODES.add_class(Emph)