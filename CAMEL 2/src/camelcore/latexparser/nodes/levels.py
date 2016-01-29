import re

from django.template import Template, loader

from latexbook.latexparser.nodes.node import NodeHTML

from latexbook.latexparser.nodes.levels import (
    Book as OriginalBook,
    Chapter as OriginalChapter,
    Section as OriginalSection,
    Subsection as OriginalSubsection
)


class Book(OriginalBook):
    """The root node level for the entire tree."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Book, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_level_book'><h1>Book</h1>",
            process_children=True,
            suffix_text="</div>"
        )


class Chapter(OriginalChapter):
    """A chapter level node - has the second highest rank."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Chapter, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        title_nodes = arguments[0].get_children()
        title_html = loader.render_to_string(
            template_name="latexbook/recurselatextree.html",
            context={"root_node": title_nodes}
        )

        return NodeHTML(
            prefix_text="<div class='latex_level_chapter'><h2>" + title_html + "</h2>",
            process_children=True,
            suffix_text="</div>"
        )


class Section(OriginalSection):
    """A section level node - has the third highest rank."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Section, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_level_section'><h3>Section</h3>",
            process_children=True,
            suffix_text="</div>"
        )


class Subsection(OriginalSubsection):
    """A subsection level node - has the fourth highest rank."""
    
    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Subsection, self).__init__(children=children)

    @classmethod
    def to_html(cls, arguments=None):
        """Called when we want to convert this node into HTML. Returns an instance of 'NodeHTML'."""
        return NodeHTML(
            prefix_text="<div class='latex_level_subsection'><h4>Subsection</h4>",
            process_children=True,
            suffix_text="</div>"
        )