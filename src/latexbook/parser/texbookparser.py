import re
from collections import namedtuple


class TexBookParser(object):
    """
    Parses components of a LaTeX book document into various objects for Python to utilise.
    """

    PreambleCapture = namedtuple("PreambleCapture", "key pattern")

    def __init__(self, nodes, preamble_captures=None):
        """Initialises the TexParser object."""
        self.nodes = nodes

        if preamble_captures is None:
            preamble_captures = [
                # PreambleCapture("module_code", r'\\modulecode\{(\w+)\}'),
                # PreambleCapture("academic_year", r'\\academicyear\{(\w+)\}'),
                # PreamblCapture("module_title", r'\\moduletitle\{(\w+)\}'),
                self.PreambleCapture(key="book_number", pattern=re.compile(r"\\booknumber\{(.*)\}")),
                self.PreambleCapture(key="book_title", pattern=re.compile(r"\\booktitle\{(.*)\}")),
                self.PreambleCapture(key="book_author", pattern=re.compile(r"\\bookauthor\{(.*)\}")),
                self.PreambleCapture(key="book_version", pattern=re.compile(r"\\bookversion\{(.*)\}")),

                # If this regex can also capture '\def\CAPTUREME{MeToo}', that'd be cool...
                self.PreambleCapture(key="new_command", pattern=re.compile(r"\\newcommand\{(.+)\}\{(.+)\}"))
            ]
        self.preamble_captures = preamble_captures

    def parse(self, latex_text):
        """
        Converts the given LaTeX document text into a Python-friendly Book object.
        """
        # Remove comments.
        latex_text = self.prepare_latex_text(latex_text)

        # Read and parse the LaTeX body.
        body = self.read_body(latex_text)

        root_node = self.nodes.get_class(self.nodes.root_node_id)
        root_node = root_node()
        root_node.add_children(self.parse_latex(body))

        # Read and parse the LaTeX preamble data.
        preamble = self.read_preamble(latex_text)
        preamble_data = self.parse_preamble(preamble)

        # Attach the preamble data onto the book.
        root_node.preamble_data = preamble_data

        return root_node

    def parse_file(self, filepath):
        """
        A convenience function for parsing a LaTeX file into a Python-friendly Book object.
        """
        with open(filepath) as f:
            latex_text = f.read()
            return self.parse(latex_text)

    def prepare_latex_text(self, latex_text):
        """
        Prepare the LaTeX text for parsing. This includes tasks such as removing the comments.
        """
        # Strip the leading and trailing whitespace characters.
        latex_text = latex_text.strip()

        # Go through the file, line by line, removing the comments.
        pattern = re.compile(r"\%.*$")
        lines = latex_text.strip().split("\n")
        for idx in range(len(lines)):
            lines[idx] = re.sub(pattern, "", lines[idx])
        latex_text = "\n".join(lines)

        # We'll implement this better later...
        # fixes = [
        #     [r'\\bit\s+', r'\\begin{itemize} '],
        #     [r'\\eit\s+', r'\\end{itemize} '],
        #     [r'\\ben\s+', r'\\begin{enumerate} '],
        #     [r'\\een\s+', r'\\end{enumerate} '],
        #     [r'\\it\s+', r'\\item '],
        #     [r'  ', r' ']
        # ]
        # for fix in fixes:
        #     latex_text = re.sub(fix[0], fix[1], latex_text)

        return latex_text

    def read_preamble(self, latex_text):
        """Returns the preamble for the given LaTeX text."""
        pattern = re.compile(r"(.*)\\begin\{document\}", re.DOTALL)
        match = re.search(pattern, latex_text)
        preamble = match.group(1) if match else ""
        return preamble

    def read_body(self, latex_text):
        """Returns the body for the given LaTeX text."""
        pattern = re.compile(r"\\begin\{document\}(.*)\\end\{document\}", re.DOTALL)
        match = re.search(pattern, latex_text)
        body = match.group(1) if match else ""
        return body

    def parse_preamble(self, preamble):
        """Parses the preamble text to collect the data."""
        # Dictionary to contain preamble properties and their declared values.
        preamble_data = {}

        # Capture a bunch of stuff from the preamble.
        for the_capture in self.preamble_captures:
            key = the_capture.key
            regex = the_capture.pattern
            pattern_obj = re.compile(regex)
            groups = re.findall(pattern_obj, preamble)
            for values in groups:
                if key in preamble_data:
                    if not isinstance(preamble_data[key], list):
                        preamble_data[key] = [preamble_data[key]]
                    preamble_data[key].append(values)
                else:
                    preamble_data[key] = values

        return preamble_data

    def parse_latex(self, latex):
        """
        Takes the contents of '\begin{document} ... \end{document}' and generates an tree object representation.
        This method returns the immediate children of the document, with each node holding pointers to
        their own children.

        We leave all detection of the start/end of nodes to the nodes themselves, this allows us to extend
        the parser without further complicating this method. It also opens the door to being able to parse
        more complex LaTeX files as we can abandon the use of Regex, allowing us correctly detect
        commands - such as a italic text within a level node's title argument.

        The logic for this method is fairly simple:
        We go through the inputted LaTeX, checking for matches with each node configured for use in the
        parser. These positive matches are then sorted in order of appearance.

        Next, we begin to iterate over the matches. During each iteration, we work out the parent of the
        current match. This is done using a while loop and a stack. Each time we pop out a level, we be
        sure to create a new Text node and fill its content with all text between the current node and the
        last match.

        We now check that the parent is allowed children. We also check that the current match does not
        occur prior to the start of the parent. The reason for this is described later on...

        We now create an instance of the match's node and recurse through its arguments, making sure that
        they're valid. If the current argument is valid, we make a recursive call and parse the arguments
        content string into this method - giving us a Python object representation. We make these objects
        children of a new Argument node, which itself is to be made a child of the current node.

        Similar to earlier in the stack, we create a new Text node and fill its content with everything
        since the last match, or since the end of the most recently popped stack node.

        If the stack is empty, the new Text node is of the highest level and should be appended to the
        list of children. Otherwise, it should be made a child of the item sitting ontop of the stack.
        We now add the current match's node using the same reasoning and push it onto the stack.

        Once we've iterated over each match, we pop everything off the stack creating Text nodes for
        any remaining text. When the stack is empty, we create a Text node for all - if any - text left
        unprocessed.
        """
        children = []

        # Ignore latex if it's just whitespace
        if not latex.isspace():
            text_node_class = self.nodes.get_class(self.nodes.text_node_id)

            # Get every node class and the matches for it.
            NodeMatch = namedtuple("NodeMatch", "node match")

            node_matches = []
            for node_id, node in self.nodes.node_classes.items():
                if node.checkable:
                    matches = node.check_latex(latex, self.nodes)
                    for match in matches:
                        node_match = NodeMatch(node=node, match=match)
                        node_matches.append(node_match)

            last_match_index = 0

            if len(node_matches) > 0:
                # Sort in the order of match appearance first.
                node_matches.sort(key=lambda x: x.match.outer_start_index)

                stack = []
                for node_match in node_matches:
                    # If the stack is populated, keep popping off items until the current node ends within the
                    # bounds of the node at the top of the stack.
                    while len(stack) > 0 and node_match.match.inner_end_index > stack[-1].match.inner_end_index:
                        remaining_text_start_idx = max(last_match_index, stack[-1].match.inner_start_index)
                        remaining_text = latex[remaining_text_start_idx:stack[-1].match.inner_end_index]
                        if text_node_class.validate_content(remaining_text):
                            text_node = text_node_class(content=remaining_text)
                            stack[-1].node.add_child(text_node)
                        last_match_index = stack[-1].match.outer_end_index
                        stack.pop()

                    # Only process this match if the stack is empty OR that the parent is allowed children
                    # and the node isn't before the parent (top of stack).
                    if (len(stack) == 0 or (
                            stack[-1].node.allowed_children and
                            node_match.match.inner_start_index > stack[-1].match.inner_start_index)):

                        # Create the node.
                        current_node = node_match.node()

                        # Check the node for arguments and their validity.
                        # If valid arguments exists, create an Argument node and make a
                        # recursive call to this function.
                        for argument in node_match.match.arguments:
                            if current_node.validate_arguments(argument):
                                argument_children = self.parse_latex(argument)
                                if len(argument_children) > 0:
                                    argument_node_class = self.nodes.get_class(self.nodes.argument_node_id)
                                    argument_node = argument_node_class()
                                    argument_node.add_children(argument_children)
                                    current_node.add_child(argument_node)

                        # If we have jumped over some text, add it to a Text node. And make it a child.
                        previous_text = latex[last_match_index:node_match.match.outer_start_index]
                        if text_node_class.validate_content(previous_text):
                            text_node = text_node_class(content=previous_text)
                            if len(stack) > 0:
                                stack[-1].node.add_child(text_node)
                            else:
                                children.append(text_node)

                        # If the stack isn't empty, make 'current_node' a child of the node on the top of the stack.
                        # If the stack is empty, append 'current_node' to the children's list.
                        if len(stack) > 0:
                            stack[-1].node.add_child(current_node)
                        else:
                            children.append(current_node)

                        last_match_index = node_match.match.inner_start_index

                        # Push the 'current_node' and node_match.match onto the stack.
                        node_instance_match = NodeMatch(node=current_node, match=node_match.match)
                        stack.append(node_instance_match)

                # Get any remaining after text.
                while len(stack) > 0:
                    after_text_start_idx = max(last_match_index, stack[-1].match.inner_start_index)
                    after_text = latex[after_text_start_idx:stack[-1].match.inner_end_index]
                    if text_node_class.validate_content(after_text):
                        text_node = text_node_class(content=after_text)
                        stack[-1].node.add_child(text_node)

                    last_match_index = stack[-1].match.outer_end_index + 1
                    stack.pop()

            # Get any remaining text.
            final_text = latex[last_match_index:len(latex)]
            if text_node_class.validate_content(final_text):
                text_node = text_node_class(content=final_text)
                children.append(text_node)

        return children
