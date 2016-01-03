import re

from ..node import Node


class EnvironmentNode(Node):
    the_type = "environment"

    """An abstract class which extends BlockNode."""
    def __init__(self, children=None):
        """Initialise the environment node."""
        super(EnvironmentNode, self).__init__(children=children)

    @classmethod
    def get_start_regex(cls):
        """Returns the regular expression used to match the start command of the environment."""
        return r"\\begin\{%s\}" % (cls.get_id())

    @classmethod
    def get_end_regex(cls):
        """Returns the regular expression used to match the end command of the environment."""
        return r"\\end\{%s\}" % (cls.get_id())

    @classmethod
    def check_latex(cls, latex, nodes):
        """
        This classmethod analyses the given latex, returning an instance of the 'CheckLatexReturn' namedtuple if
        a match is found - else it should return None.
        As an environment is surrounded between a \begin{...} and an \end{...}, we must capture the latex bounded
        between the two commands.
        """
        latex_matches = []

        start_regex = cls.get_start_regex()
        end_regex = cls.get_end_regex()
        regex = re.compile("(" + start_regex + ")|(" + end_regex + ")")

        matches = re.finditer(regex, latex)

        # Prepare our match indexes as we're iterating over both \begin{...} and \end{...} commands.
        inner_start_index = None
        inner_end_index = None
        outer_start_index = None
        outer_end_index = None

        # In the case an environment contains another instance of itself, we must avoid considering the nested's
        # instance \end{...} command. This counter allows us to correctly pair the \start{...} command with the
        # appropriate \end{...}.
        counter = 0

        # Iterate through the matches.
        for match in matches:
            start_index = match.start()
            match_str = match.group(0)
            arguments = match.groups()
            is_start_match = arguments[0] is not None  # Is this a start or end match?
            arguments = arguments[2:]  # The first two groups AREN'T arguments.

            if is_start_match:
                counter += 1

                outer_start_index = start_index
                inner_start_index = outer_start_index + len(match_str)
            else:
                counter -= 1

                inner_end_index = start_index
                outer_end_index = inner_end_index + len(match_str)

                # Is this the paired end match?
                if counter == 0:
                    latex_matches.append(cls.CheckLatexReturn(
                        inner_start_index=inner_start_index,
                        inner_end_index=inner_end_index,
                        outer_start_index=outer_start_index,
                        outer_end_index=outer_end_index,
                        arguments=arguments
                    ))
        return latex_matches
