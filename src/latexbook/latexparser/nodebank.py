class NodeBank(object):
    """Holds together all our nodes classes - providing several functions to navigate through them."""

    def __init__(self):
        self.node_classes = {}
        self.root_node_id = None
        self.text_node_id = None
        self.argument_node_id = None

    def add_class(self, node_class):
        """Adds the given node class to our node list."""
        self.node_classes[node_class.get_id()] = node_class

    def get_class(self, node_id):
        """Returns the node class with the given node ID."""
        return self.node_classes.get(node_id)

    def set_root_node_id(self, node_id):
        """Sets the root node."""
        node = self.get_class(node_id)
        if node is not None:
            self.root_node_id = node_id
        return node

    def set_text_node_id(self, node_id):
        """Sets the node used for plain-text."""
        node = self.get_class(node_id)
        if node is not None:
            self.text_node_id = node_id
        return node

    def set_argument_node_id(self, node_id):
        """Sets the node used for arguments."""
        node = self.get_class(node_id)
        if node is not None:
            self.argument_node_id = node_id
        return node

    def get_by_attr(self, node_attr):
        """Returns all the node classes which contain an attribute with the given name."""
        found_nodes = []
        for node_id, node in self.node_classes.items():
            if hasattr(node, node_attr):
                found_nodes.append(node)
        return found_nodes
