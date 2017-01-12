from node import Node

class Stack: 
    
    def __init__(self):
        top = None
        
    def pop():
        if top is None:
            raise AssertionError("cannot pop empty stack")
        my_top = top
        top = top.get_next()
        return my_top.get_value()
    
    def push(item):
        new_top = Node(v=item)
        new_top.set_next(top)
        top = new_top
    
    def peek():
        return top.get_value()
    
    def is_empty():
        return top == None
        