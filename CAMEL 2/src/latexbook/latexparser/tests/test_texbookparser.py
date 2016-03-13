"""Contains unit-tests regarding texbookparser.py.

As our LaTeX Parser is completely decoupled from our Django project, these tests must make no reference to any code
outside the scope of this package.

Check here for information on writing and running tests:
https://docs.python.org/3/library/unittest.html
"""

import unittest

from .config.experimental_nodebank import BOOKNODES
from ..texbookparser import TexBookParser

# For convenience, get all our Node classes here:
# Get Misc nodes
Node_Text = BOOKNODES.get_class(BOOKNODES.text_node_id)
Node_Argument = BOOKNODES.get_class(BOOKNODES.argument_node_id)

# Get Command Node
Node_TextIt = BOOKNODES.get_class("textit")
Node_Emph = BOOKNODES.get_class("emph")

# Get Environment Nodes
Node_Proof = BOOKNODES.get_class("proof")
Node_Verbatim = BOOKNODES.get_class("verbatim")

# Get Level Nodes
Node_Book = BOOKNODES.get_class("book")
Node_Chapter = BOOKNODES.get_class("chapter")
Node_Section = BOOKNODES.get_class("section")
Node_Subsection = BOOKNODES.get_class("subsection")


# Build parser instance
tex_book_parser = TexBookParser(BOOKNODES)


# NOTE:
# Because this class extends 'unittest.TestCase' it isn't
# safe to test any database functionality.
# Instead, use the 'TestParserAdapter' class which is below.
class TestParseLatex(unittest.TestCase):
    """Tests the method 'TexBookParser.parse_latex'."""

    def test_nodes_command_nested(self):
        """Test if the parser works correctly when one command node is nested inside another."""
        # Get LaTeX string to test
        test_latex_string = r"\textit{Hello \emph{World}}"

        # Create the Node components
        italic = Node_TextIt()
        emph = Node_Emph()
        italic_text = Node_Text("Hello ")
        italic_emph_text = Node_Text("World")

        # Form the tree.
        italic.add_child(italic_text)
        italic.add_child(emph)
        emph.add_child(italic_emph_text)

        correct_structure = [italic]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))
