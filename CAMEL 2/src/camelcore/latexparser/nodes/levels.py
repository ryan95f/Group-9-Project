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


class Chapter(OriginalChapter):
    """A chapter level node - has the second highest rank."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Chapter, self).__init__(children=children)


class Section(OriginalSection):
    """A section level node - has the third highest rank."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Section, self).__init__(children=children)


class Subsection(OriginalSubsection):
    """A subsection level node - has the fourth highest rank."""

    def __init__(self, children=None):
        """Initialise the section level node."""
        super(Subsection, self).__init__(children=children)
