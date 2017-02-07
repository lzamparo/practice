class BinaryTreeNode(object):
    def __init__(self,value=None):
        self.left = None
        self.right = None
        self.value = value
        self.visited = False
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        
    def set_left(self, node):
        self.left = node
        
    def set_right(self, node):
        self.right = node
        
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right
    
    def visit(self):
        self.visited = True
        print(self.value)
        
    