# Probably best not to worry about this here...
# flake8: noqa

"""
To avoid over-complicating our base settings file, our LaTeXBook settings get their own file!
This module simply defines each Node that we intend to capture when parsing a LaTeX document body.

For the sake of convenience, I shall try to briefly describe the logic behind how the LaTeXBook application works...
There are two 'main' types of nodes; a node which just holds plain-text and a node which 'may' be the parent of a
plain-text node. These parent nodes shall be referred to as book-nodes and they include things such as:
Chapters, Sections, Include-Graphics, Text-Styles, Arguments etc...

In an ordinary LaTeX document, there are three identifiable types of commands:
    - Regular Commands: A standard LaTeX command which is often presented following format:
        \\commandname{commandarguments}

        These include:
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

        These include:
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

import os

# Import our 'Nodes' class.
from latexbook.latexparser.nodebank import (
    NodeBank
)

# Import all the nodes that we want the parser to utilise.
from camelcore.apps.latexbook.latexparser.nodes.node import (
    ArgumentNode, TextNode
)

from camelcore.apps.latexbook.latexparser.nodes.levels import (
    Book, Chapter, Section, Subsection
)

from camelcore.apps.latexbook.latexparser.nodes.environments.box import (
    Proof, Verbatim, Center
)

from camelcore.apps.latexbook.latexparser.nodes.environments.float import (
    Figure, Subfigure, Table, Subtable,
)

from camelcore.apps.latexbook.latexparser.nodes.environments.list import (
    Itemize, Enumerate
)

from camelcore.apps.latexbook.latexparser.nodes.environments.mathmode import (
    Equation, EqnArray, Cases, Align, Array
)

from camelcore.apps.latexbook.latexparser.nodes.environments.theorem import (
    Theorem, Lemma, Corollary, Definition, Remark, Example, Exercise
)

from camelcore.apps.latexbook.latexparser.nodes.commands.content import (
    Image
)

from camelcore.apps.latexbook.latexparser.nodes.commands.reference import (
    Reference, Citation, Label
)

from camelcore.apps.latexbook.latexparser.nodes.commands.textstyles import (
     Emph, TextBf, TextIt,  Underline
)

from camelcore.apps.latexbook.latexparser.nodes.commands.item import (
    Item
)

# Import our HomeworkQuiz nodes.
from camelcore.apps.homeworkquiz.latexbook.latexparser.nodes.commands.choice import (
    Choice, CorrectChoice, TextAnswer
)

from camelcore.apps.homeworkquiz.latexbook.latexparser.nodes.environments.homework import (
    Homework, Quiz, QuizQuestion
)

from camelcore.apps.homeworkquiz.latexbook.latexparser.nodes.environments.questiontypes import (
    SingleChoice, MultipleChoice, MathjaxText
)


# Create the dictionary used to get node templates.
LATEX_NODE_TEMPLATE_PATHS = {}

# This is used to configure our parser, so that we only get build a tree using the nodes we're interested in.
BOOKNODES = NodeBank()

def add_node_quick(dir, node):
    """A quick way to add a node into the system."""
    BOOKNODES.add_class(node)
    LATEX_NODE_TEMPLATE_PATHS[node.get_id()] = os.path.join(dir, node.get_id() + ".html")

def add_nodes_quick(dir, node_list):
    """A wrapper around 'add_node_quick' to take an array of nodes."""
    [add_node_quick(dir, node) for node in node_list]

# Add argument node.
BOOKNODES.add_class(ArgumentNode)
BOOKNODES.set_argument_node_id(ArgumentNode.get_id())

LB_NODE_ROOT = "camelcore/apps/latexbook/latexparser/nodes"

# Add content text node.
add_node_quick(os.path.join(LB_NODE_ROOT, "misc"), TextNode)
BOOKNODES.set_text_node_id(TextNode.get_id())

# Add level nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "levels"), [Book, Chapter, Section, Subsection])
BOOKNODES.set_root_node_id(Book.get_id())

# Add box environment nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "environments/box"), [Proof, Verbatim, Center])

# Add float environment nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "environments/float"), [Figure, Subfigure, Table, Subtable])

# Add list environment nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "environments/list"), [Itemize, Enumerate])

# Add mathmode environment nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "environments/mathmode"), [Equation, EqnArray, Cases, Align, Array])
# Add theorem environment nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "environments/theorem"), [Theorem, Lemma, Corollary, Definition, Remark, Example, Exercise])

# Add content command nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "commands/content"), [Image])

# Add list command nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "commands/list"), [Item])

# Add reference command nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "commands/reference"), [Reference, Citation, Label])

# Add text-style command nodes.
add_nodes_quick(os.path.join(LB_NODE_ROOT, "commands/textstyles"), [Emph, TextBf, TextIt, Underline])


# BEGIN HomeworkQuiz Setup.
HQ_NODE_ROOT = "camelcore/apps/homeworkquiz/latexbook/latexparser/nodes"

# Add homework environment nodes.
add_nodes_quick(os.path.join(HQ_NODE_ROOT, "environments/homework"), [Homework, Quiz, QuizQuestion])

# Add questiontypes environment nodes.
add_nodes_quick(os.path.join(HQ_NODE_ROOT, "environments/questiontype"), [SingleChoice, MultipleChoice, MathjaxText])

# Add choice command nodes.
add_nodes_quick(os.path.join(HQ_NODE_ROOT, "commands/choice"), [Choice, CorrectChoice, TextAnswer])
