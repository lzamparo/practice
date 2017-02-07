from stack import Stack
from node import Node

class MyQueue(object):
    ''' A queue that is implemented via two stacks.  Enqueue by pushing onto the new stack, dequeue by moving all data from new to old stack, and popping from the old stack '''
    
    def __init__(self):
        self.new_stack = Stack()
        self.old_stack = Stack()
        
    def enqueue(self, item):
        self.new_stack.push(item)
    
    
    def dequeue(self):
        self._move_new_to_old()
        return self.old_stack.pop()
        
    
    def peek(self):
        self._move_new_to_old()
        return self.old_stack.peek()
    

    def is_empty(self):
        return self.primary_stack.is_empty() and self.secondary_stack.is_empty()
    
    
    def _move_new_to_old(self):
        if self.old_stack.is_empty():
            while not self.new_stack.is_empty():
                self.old_stack.push(self.new_stack.pop())
    
    