import re

from .node import Node


class CommandNode(Node):
    """A node which gives some Text, or other commands, a semantic meaning."""

    the_type = "command"

    def __init__(self, children=None):
        """Initialise the command Node."""
        super(CommandNode, self).__init__(children=children)

    @classmethod
    def get_start_regex(cls):
        """Return the regular expression used to match the start command of the environment."""
        return re.compile(r"\\%s\{" % (cls.get_id()))

    @classmethod
    def check_latex(cls, latex, nodes):
        """Analyse the given LaTeX text, returning a list of all matches (CheckLatexReturn)."""
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
