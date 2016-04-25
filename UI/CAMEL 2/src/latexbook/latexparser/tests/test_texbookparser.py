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
    
    def test_nodes_level_section(self):
        """Test if the parser works correctly for the section node."""
        # Get LaTeX string to test
        test_latex_string = r"\section{Hello}"

        # Create the Node components
        section = Node_Section()
        argument = Node_Argument()
        section_text = Node_Text("Hello")

        # Form the tree.
        section.add_child(argument)
        argument.add_child(section_text)

        correct_structure = [section]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))
    
    def test_nodes_level_subsection(self):
        """Test if the parser works correctly for the subsection node."""
        # Get LaTeX string to test
        test_latex_string = r"\subsection{Hello}"

        # Create the Node components
        subsection = Node_Subsection()
        argument = Node_Argument()
        subsection_text = Node_Text("Hello")

        # Form the tree.
        subsection.add_child(argument)
        argument.add_child(subsection_text)

        correct_structure = [subsection]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))
    
    def test_nodes_environment_verbatim(self):
        """Test if the parser works correctly for the verbatim nodes."""
        # Get LaTeX string to test
        test_latex_string = r"\begin{verbatim} Hello \end{verbatim}"

        # Create the Node components
        verbatim = Node_Verbatim()
        verbatim_text = Node_Text("Hello")

        # Form the tree.
        verbatim.add_child(verbatim_text)

        correct_structure = [verbatim]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))
    
    def test_nodes_environment_proof(self):
        """Test if the parser works correctly for the proof nodes."""
        # Get LaTeX string to test
        test_latex_string = r"\begin{proof} Hello \end{proof}"

        # Create the Node components
        proof = Node_Proof()
        proof_text = Node_Text("Hello")

        # Form the tree.
        proof.add_child(proof_text)

        correct_structure = [proof]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))

    def test_nodes_command_Italic(self):
        test_latex_string = r"\textit{Hello World}"

        italic = Node_TextIt()
        italic_text = Node_Text("Hello World")

        italic.add_child(italic_text)

        correct_structure = [italic]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))

    def test_nodes_Emphasis(self):
        test_latex_string = r"\emph{Hello World}"
    
        emphasis = Node_Emph()
        emph_text = Node_Text("Hello World")

        emphasis.add_child(emph_text)

        correct_structure = [emphasis]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))

    def test_nodes_command_book(self):
        """test if parser works correectly with books"""
        test_latex_string = r"\book{Hello World}"

        book = Node_Book()
        book_content = Node_Argument()
        book_text = Node_Text("Hello World")

        book.add_child(book_content)
        book_content.add_child(book_text)

        correct_structure = [book]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))

    def test_nodes_command_Chapter(self):
        test_latex_string = r"\chapter{Hello World}"

        Chapter = Node_Chapter()
        Chapter_content = Node_Argument()
        Chapter_text = Node_Text("Hello World")

        Chapter.add_child(Chapter_content)
        Chapter_content.add_child(Chapter_text)

        correct_structure = [Chapter]
        test_structure = tex_book_parser.parse_latex(test_latex_string)

        return self.assertEqual(repr(correct_structure), repr(test_structure))
