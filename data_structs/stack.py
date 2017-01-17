from node import Node

class Stack(object): 
    
    def __init__(self):
        self.top = None
        
    def pop(self):
        if self.top == None:
            raise AssertionError("cannot pop empty stack")
        my_top = self.top
        self.top = self.top.get_next()
        return my_top.get_value()
    
    def push(self,item):
        new_top = Node(v=item)
        new_top.set_next(self.top)
        self.top = new_top
    
    def peek(self):
        if self.is_empty():
            raise AssertionError("stack is empty")
        return self.top.get_value()
    
    def is_empty(self):
        return self.top == None
        