from node import Node
from stack import Stack

class min_Stack(object):
    
    def __init__(self):
        self.min_stack = Stack()
        self.top = None
        
    def push(self,item):
        new_top = Node(v=item)
        new_top.set_next(self.top)
        self.top = new_top
        if self.min_stack.is_empty():
            self.min_stack.push(item)
        else:
            if item <= self.min_stack.peek():
                self.min_stack.push(item)
    
    def pop(self):
        if self.top == None:
            raise AssertionError("cannot pop empty stack")
        my_top = self.top
        self.top = self.top.get_next()
        value = my_top.get_value()
        if value == self.min_stack.peek():
            self.min_stack.pop()
        return value

    def min(self):
        return self.min_stack.peek()
        
    def is_empty(self):
        return self.top == None    
    
    def peek(self):
        if self.is_empty():
            raise AssertionError("stack is empty")
        return self.top.get_value()    