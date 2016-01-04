"""
To avoid over-complicating our base settings file, our LaTeXBook settings get their own file!
This module simply defines each Node that we intend to capture when parsing a LaTeX document body.

For the sake of conveinence, I shall try to briefly describe the logic behind how the LaTeXBook application works...
There are two 'main' types of nodes; a node which just holds plain-text and a node which 'may' be the parent of a
plain-text node. These parent nodes shall be refered to as book-nodes and they include things such as:
Chapters, Sections, Include-Graphics, Text-Styles, Arguments etc...

In an ordinary LaTeX document, there are three identifiable types of commands:
    - Regular Commands: A standard LaTeX command which is often presented following format:
        \\commandname{commandarguments}

        These inlcude:
        Include-Graphics, Reference, Label, Text-Styles etc...

    - Level Commands: A regular command which becomes the parent of all below commands and text until another level
        command is reached that has a higher, or equal to, rank.
        Inside the curly braces of the level command is defined the level's title. This could be any number of
        regular commands. To make this easily representable, all book-node arguments are defined in a special argument
        node which shall be discussed later.

        These include:
        Chapters, Sections, SubSections etc...

    - Environment Commands: An environment is similar to a level command, except its contents end with a explicitly
        defined end block.

        These inlcude:
        Proof, Figure, Itemize, Theorem etc...

The parser checks the document against each node to locate all matches. This allows the logic behind how a node works
to be decoupled from the parser - making it ideal for keeping things simple and to spread the workload amongst a team
of people.

When a node is checked, it will inform the parser of any additional arguments. These additional arguments are
parsed through recursive calls to the parser. This grants us the benefit of having to not overcomplicate our code any
further.

Once we have a sub-tree for each argument, we create a special argument node which shall be the root of this sub-tree.
This argument node is added as a child to the recently checked node.

It is the responsibility of the view to render this tree as intended.

For more information regarding the parser, refer to 'latexbook/latexparser/texbookparser.py'.
"""

# Import our 'Nodes' class.
from latexbook.latexparser.nodes import (
    Nodes
)

# Import all the nodes that we want the parser to utilise.
from latexbook.latexparser.nodes.node import (
    ArgumentNode, Text
)

from latexbook.latexparser.nodes.levels import (
    Book, Chapter, Section, Subsection
)

from latexbook.latexparser.nodes.environments.box import (
    Proof, Verbatim, Center
)

from latexbook.latexparser.nodes.environments.float import (
    Figure, Subfigure, Table, Subtable,
)

from latexbook.latexparser.nodes.environments.list import (
    Itemize, Enumerate
)

from latexbook.latexparser.nodes.environments.mathmode import (
    Equation, EqnArray, Cases, Align, Array
)

from latexbook.latexparser.nodes.environments.theorem import (
    Theorem, Lemma, Corollary, Definition, Remark, Example, Exercise
)

from latexbook.latexparser.nodes.commands.content import (
    Image
)

from latexbook.latexparser.nodes.commands.reference import (
    Reference, Citation, Label
)

from latexbook.latexparser.nodes.commands.textstyles import (
    TextIt, TextBf, Underline, Emph
)

from latexbook.latexparser.nodes.commands.item import (
    Item
)

# This is used to configure our parser, so that we only get build a tree using the nodes we're interested in.
BOOKNODES = Nodes()

# Add argument node.
BOOKNODES.add_class(ArgumentNode)
BOOKNODES.set_argument_node_id(ArgumentNode.get_id())

# Add content text node.
BOOKNODES.add_class(Text)
BOOKNODES.set_text_node_id(Text.get_id())

# Add level nodes.
BOOKNODES.add_class(Book)
BOOKNODES.set_root_node_id(Book.get_id())
BOOKNODES.add_class(Chapter)
BOOKNODES.add_class(Section)
BOOKNODES.add_class(Subsection)

# Add box environment nodes.
BOOKNODES.add_class(Proof)
BOOKNODES.add_class(Verbatim)
BOOKNODES.add_class(Center)

# Add float environment nodes.
BOOKNODES.add_class(Figure)
BOOKNODES.add_class(Subfigure)
BOOKNODES.add_class(Table)
BOOKNODES.add_class(Subtable)

# Add list environment nodes.
BOOKNODES.add_class(Itemize)
BOOKNODES.add_class(Enumerate)

# Add mathmode environment nodes.
BOOKNODES.add_class(Equation)
BOOKNODES.add_class(EqnArray)
BOOKNODES.add_class(Cases)
BOOKNODES.add_class(Align)
BOOKNODES.add_class(Array)

# Add theorem environment nodes.
BOOKNODES.add_class(Theorem)
BOOKNODES.add_class(Lemma)
BOOKNODES.add_class(Corollary)
BOOKNODES.add_class(Definition)
BOOKNODES.add_class(Remark)
BOOKNODES.add_class(Example)
BOOKNODES.add_class(Exercise)

# Add content command nodes.
BOOKNODES.add_class(Image)

# Add list command nodes.
BOOKNODES.add_class(Item)

# Add reference command nodes.
BOOKNODES.add_class(Reference)
BOOKNODES.add_class(Citation)
BOOKNODES.add_class(Label)

# Add text style command nodes.
BOOKNODES.add_class(TextIt)
BOOKNODES.add_class(TextBf)
BOOKNODES.add_class(Underline)
BOOKNODES.add_class(Emph)
