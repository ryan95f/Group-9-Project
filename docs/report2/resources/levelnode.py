import re

from .node import Node
from .util.getpairedregex import get_paired_regex


class LevelNode(Node):
    """An abstract class which extends BlockNode, by implementing a rank hierarchy."""
    is_level_node = True  # So we can get ALL level nodes.

    # We determine a hierarchical order for the level nodes,
    # so we can correctly create the tree.
    # Lower values represent a more-superior rank.
    rank = 0

    def __init__(self, children=None):
        """Initialise the level node."""
        super(LevelNode, self).__init__(children=children)

    @classmethod
    def get_start_regex(cls):
        """Returns the regular expression used to match the start command of the level node."""
        return re.compile(r"\\%s\{" % (cls.get_id()))

    @classmethod
    def check_latex(cls, latex, nodes):
        """
        This classmethod analyses the given latex, returning an instance of the 'CheckLatexReturn' namedtuple if
        a match is found - else it should return None.
        """
        start_regex = cls.get_start_regex()
        argument_start_regex = r"{"
        argument_end_regex = r"}"

        start_matches = re.finditer(start_regex, latex)

        latex_matches = []

        # Test only the first match.
        for match in start_matches:
            start_index = match.start()
            match_str = match.group(0)

            outer_start_index = start_index
            inner_end_index = len(latex) - 1
            outer_end_index = inner_end_index

            # As the title for a LaTeX level node is held within the curly braces and could
            # contain others nodes, we can't safely use regex to obtain the contents due to not
            # being able to get the paired end curly braces. So, we do this manually.
            argument_text_start_index = start_index + len(match_str)
            argument_text_inner_end_index, argument_text_outer_end_index = get_paired_regex(
                latex[argument_text_start_index:], argument_start_regex, argument_end_regex
            )
            inner_start_index = argument_text_outer_end_index + argument_text_start_index
            arguments = (latex[argument_text_start_index:inner_start_index-1], )

            # Check the current match against all other levels. This is done so we can get the end-index to not go past
            # any LevelNode of a superior rank.
            superior_nodes = [x for x in nodes.get_by_attr("is_level_node") if x.rank <= cls.rank]
            for superior_node in superior_nodes:
                superior_start_regex = superior_node.get_start_regex()
                superior_start_matches = re.finditer(superior_start_regex, latex)
                for superior_match in superior_start_matches:
                    superior_match_start = superior_match.start()
                    if superior_match_start < inner_end_index and superior_match_start > inner_start_index:
                        inner_end_index = superior_match_start

            outer_end_index = inner_end_index

            # Is this the paired end match?
            latex_matches.append(cls.CheckLatexReturn(
                inner_start_index=inner_start_index,
                inner_end_index=inner_end_index,
                outer_start_index=outer_start_index,
                outer_end_index=outer_end_index,
                arguments=arguments
            ))

        return latex_matches
