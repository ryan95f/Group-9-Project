import re

from ..node import Node, LeafNode


class Text(LeafNode):
    """A leaf node which just holds some plain text."""

    the_type = "text"

    def __init__(self, content):
        """Initialise the text leaf node."""
        super(Text, self).__init__()
        self.set_content(content)

    def __str__(self):
        """Returns a nicely printable string of the node."""
        return self.content

    def __repr__(self):
        """Return the canonical string representation of the node."""
        return "%s(\"%s\")" % (self.__class__.__name__, self.content)

    @classmethod
    def validate_content(cls, content):
        """Returns a boolean indicating if the content is acceptable for the Text node."""
        return content == " " if content.isspace() else content != ""

    def set_content(self, content):
        """Sets the text, allowing us to change it if needed"""
        self.content = content.strip()


class Command(Node):
    """A node which gives some Text, or other commands, a semantic meaning."""
    the_type = "command"

    def __init__(self, children=None):
        """Initialise the command Node."""
        super(Command, self).__init__(children=children)

    @classmethod
    def get_start_regex(cls):
        """Returns the regular expression used to match the start command of the environment."""
        return re.compile(r"\\%s\{" % (cls.get_id()))

    @classmethod
    def check_latex(cls, latex, nodes):
        """
        This classmethod analyses the given latex, returning an instance of the 'CheckLatexReturn' namedtuple if
        a match is found - else it should return None.
        """
        start_regex = cls.get_start_regex()

        start_matches = re.finditer(start_regex, latex)

        latex_matches = []

        # Test only the first match.
        for match in start_matches:
            start_index = match.start()
            match_str = match.group(0)
            arguments = match.groups()

            # As a command could contain other commands, we must use a counter that increments when we encounter
            # opening curly braces and decrements when we encounter closing curly braces. This allows us to determine
            # the correct braces pair.
            counter = 0

            for c_idx in range(start_index, len(latex)):
                c = latex[c_idx]
                last_char = latex[c_idx - 1] if c_idx > start_index else ""

                # Check if the current character isn't an escaped curly braces.
                if c == "{" and last_char != "\\":
                    counter += 1
                elif c == "}" and last_char != "\\":
                    counter -= 1

                    # Is this the pairs closing curly braces we're looking for.
                    if counter == 0:
                        latex_matches.append(cls.CheckLatexReturn(
                            inner_start_index=start_index + len(match_str),
                            inner_end_index=c_idx,
                            outer_start_index=start_index,
                            outer_end_index=c_idx + len("}"),
                            arguments=arguments
                        ))
                        break
        return latex_matches
