from binary_tree_node import BinaryTreeNode

class BinaryTree(object):
    
    def __init__(self):
        self.root = None
        
    def get_root(self):
        return self.root
    
    def set_root(self, node):
        self.root = node
        