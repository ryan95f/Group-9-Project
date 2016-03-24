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
from camelcore.latexparser.nodes.node import (
    ArgumentNode, TextNode
)

from camelcore.latexparser.nodes.levels import (
    Book, Chapter, Section, Subsection
)

from camelcore.latexparser.nodes.environments.box import (
    Proof, Verbatim, Center
)

from camelcore.latexparser.nodes.environments.float import (
    Figure, Subfigure, Table, Subtable,
)

from camelcore.latexparser.nodes.environments.list import (
    Itemize, Enumerate
)

from camelcore.latexparser.nodes.environments.mathmode import (
    Equation, EqnArray, Cases, Align, Array
)

from camelcore.latexparser.nodes.environments.theorem import (
    Theorem, Lemma, Corollary, Definition, Remark, Example, Exercise
)

from camelcore.latexparser.nodes.commands.content import (
    Image
)

from camelcore.latexparser.nodes.commands.reference import (
    Reference, Citation, Label
)

from camelcore.latexparser.nodes.commands.textstyles import (
    TextIt, TextBf, Underline, Emph
)

from camelcore.latexparser.nodes.commands.item import (
    Item
)

# Import our HomeworkQuiz nodes.
from camelcore.homeworkquiz.latexbook.latexparser.nodes.commands.choice import (
    Choice, CorrectChoice, TextAnswer
)

from camelcore.homeworkquiz.latexbook.latexparser.nodes.environments.homework import (
    Homework, Quiz, QuizQuestion
)

from camelcore.homeworkquiz.latexbook.latexparser.nodes.environments.questiontypes import (
    SingleChoice, MultipleChoice, MathjaxText
)


# Create the dictionary used to get node templates.
LATEX_NODE_TEMPLATE_PATHS = {}


# This is used to configure our parser, so that we only get build a tree using the nodes we're interested in.
BOOKNODES = NodeBank()

# Add argument node.
BOOKNODES.add_class(ArgumentNode)
BOOKNODES.set_argument_node_id(ArgumentNode.get_id())

# Add content text node.
BOOKNODES.add_class(TextNode)
BOOKNODES.set_text_node_id(TextNode.get_id())
LATEX_NODE_TEMPLATE_PATHS[TextNode.get_id()] = "latexbook/nodes/misc"

# Add level nodes.
BOOKNODES.add_class(Book)
BOOKNODES.set_root_node_id(Book.get_id())
LATEX_NODE_TEMPLATE_PATHS[Book.get_id()] = "latexbook/nodes/levels"
BOOKNODES.add_class(Chapter)
LATEX_NODE_TEMPLATE_PATHS[Chapter.get_id()] = "latexbook/nodes/levels"
BOOKNODES.add_class(Section)
LATEX_NODE_TEMPLATE_PATHS[Section.get_id()] = "latexbook/nodes/levels"
BOOKNODES.add_class(Subsection)
LATEX_NODE_TEMPLATE_PATHS[Subsection.get_id()] = "latexbook/nodes/levels"

# Add box environment nodes.
BOOKNODES.add_class(Proof)
LATEX_NODE_TEMPLATE_PATHS[Proof.get_id()] = "latexbook/nodes/environments/box"
BOOKNODES.add_class(Verbatim)
LATEX_NODE_TEMPLATE_PATHS[Verbatim.get_id()] = "latexbook/nodes/environments/box"
BOOKNODES.add_class(Center)
LATEX_NODE_TEMPLATE_PATHS[Center.get_id()] = "latexbook/nodes/environments/box"

# Add float environment nodes.
BOOKNODES.add_class(Figure)
LATEX_NODE_TEMPLATE_PATHS[Figure.get_id()] = "latexbook/nodes/environments/float"
BOOKNODES.add_class(Subfigure)
LATEX_NODE_TEMPLATE_PATHS[Subfigure.get_id()] = "latexbook/nodes/environments/float"
BOOKNODES.add_class(Table)
LATEX_NODE_TEMPLATE_PATHS[Table.get_id()] = "latexbook/nodes/environments/float"
BOOKNODES.add_class(Subtable)
LATEX_NODE_TEMPLATE_PATHS[Subtable.get_id()] = "latexbook/nodes/environments/float"

# Add list environment nodes.
BOOKNODES.add_class(Itemize)
LATEX_NODE_TEMPLATE_PATHS[Itemize.get_id()] = "latexbook/nodes/environments/list"
BOOKNODES.add_class(Enumerate)
LATEX_NODE_TEMPLATE_PATHS[Enumerate.get_id()] = "latexbook/nodes/environments/list"

# Add mathmode environment nodes.
BOOKNODES.add_class(Equation)
LATEX_NODE_TEMPLATE_PATHS[Equation.get_id()] = "latexbook/nodes/environments/mathmode"
BOOKNODES.add_class(EqnArray)
LATEX_NODE_TEMPLATE_PATHS[EqnArray.get_id()] = "latexbook/nodes/environments/mathmode"
BOOKNODES.add_class(Cases)
LATEX_NODE_TEMPLATE_PATHS[Cases.get_id()] = "latexbook/nodes/environments/mathmode"
BOOKNODES.add_class(Align)
LATEX_NODE_TEMPLATE_PATHS[Align.get_id()] = "latexbook/nodes/environments/mathmode"
BOOKNODES.add_class(Array)
LATEX_NODE_TEMPLATE_PATHS[Array.get_id()] = "latexbook/nodes/environments/mathmode"

# Add theorem environment nodes.
BOOKNODES.add_class(Theorem)
LATEX_NODE_TEMPLATE_PATHS[Theorem.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Lemma)
LATEX_NODE_TEMPLATE_PATHS[Lemma.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Corollary)
LATEX_NODE_TEMPLATE_PATHS[Corollary.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Definition)
LATEX_NODE_TEMPLATE_PATHS[Definition.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Remark)
LATEX_NODE_TEMPLATE_PATHS[Remark.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Example)
LATEX_NODE_TEMPLATE_PATHS[Example.get_id()] = "latexbook/nodes/environments/theorem"
BOOKNODES.add_class(Exercise)
LATEX_NODE_TEMPLATE_PATHS[Exercise.get_id()] = "latexbook/nodes/environments/theorem"

# Add content command nodes.
BOOKNODES.add_class(Image)
LATEX_NODE_TEMPLATE_PATHS[Image.get_id()] = "latexbook/nodes/commands/content"

# Add list command nodes.
BOOKNODES.add_class(Item)
LATEX_NODE_TEMPLATE_PATHS[Item.get_id()] = "latexbook/nodes/commands/list"

# Add reference command nodes.
BOOKNODES.add_class(Reference)
LATEX_NODE_TEMPLATE_PATHS[Reference.get_id()] = "latexbook/nodes/commands/reference"
BOOKNODES.add_class(Citation)
LATEX_NODE_TEMPLATE_PATHS[Citation.get_id()] = "latexbook/nodes/commands/reference"
BOOKNODES.add_class(Label)
LATEX_NODE_TEMPLATE_PATHS[Label.get_id()] = "latexbook/nodes/commands/reference"

# Add text-style command nodes.
BOOKNODES.add_class(TextIt)
LATEX_NODE_TEMPLATE_PATHS[TextIt.get_id()] = "latexbook/nodes/commands/textstyles"
BOOKNODES.add_class(TextBf)
LATEX_NODE_TEMPLATE_PATHS[TextBf.get_id()] = "latexbook/nodes/commands/textstyles"
BOOKNODES.add_class(Underline)
LATEX_NODE_TEMPLATE_PATHS[Underline.get_id()] = "latexbook/nodes/commands/textstyles"
BOOKNODES.add_class(Emph)
LATEX_NODE_TEMPLATE_PATHS[Emph.get_id()] = "latexbook/nodes/commands/textstyles"


# BEGIN HomeworkQuiz Setup.
HQ_NODE_ROOT = "camelcore/homeworkquiz/latexbook/latexparser/nodes"

# Add homework environment nodes.
BOOKNODES.add_class(Homework)
LATEX_NODE_TEMPLATE_PATHS[Homework.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/homework")
BOOKNODES.add_class(Quiz)
LATEX_NODE_TEMPLATE_PATHS[Quiz.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/homework")
BOOKNODES.add_class(QuizQuestion)
LATEX_NODE_TEMPLATE_PATHS[QuizQuestion.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/homework")

# Add questiontypes environment nodes.
BOOKNODES.add_class(SingleChoice)
LATEX_NODE_TEMPLATE_PATHS[SingleChoice.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/questiontype")
BOOKNODES.add_class(MultipleChoice)
LATEX_NODE_TEMPLATE_PATHS[MultipleChoice.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/questiontype")
BOOKNODES.add_class(MathjaxText)
LATEX_NODE_TEMPLATE_PATHS[MathjaxText.get_id()] = os.path.join(HQ_NODE_ROOT, "environments/questiontype")

# Add choice command nodes.
BOOKNODES.add_class(Choice)
LATEX_NODE_TEMPLATE_PATHS[Choice.get_id()] = os.path.join(HQ_NODE_ROOT, "commands/choice")
BOOKNODES.add_class(CorrectChoice)
LATEX_NODE_TEMPLATE_PATHS[CorrectChoice.get_id()] = os.path.join(HQ_NODE_ROOT, "commands/choice")
BOOKNODES.add_class(TextAnswer)
LATEX_NODE_TEMPLATE_PATHS[TextAnswer.get_id()] = os.path.join(HQ_NODE_ROOT, "commands/choice")
