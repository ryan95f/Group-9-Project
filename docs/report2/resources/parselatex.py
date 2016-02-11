class TexBookParser(object):
    """The remainder of this class has not been included in this example."""

    def parse_latex(self, latex):
            """Docstrings are as described in the above explanation..."""
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