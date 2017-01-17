from node import Node

class Queue(object):
    
    def __init__(self):
        self.head = None
        self.tail = None
    
    def remove(self):
        if not self.is_empty():
            t = self.head.get_value()
            self.head = self.head.get_next()
            if self.head is None:
                self.tail = None
            return t
        else:
            raise AssertionError("cannot pop empty queue")
    
    def add(self,item):
        end = Node(v=item)
        if self.tail is not None:
            self.tail.set_next(end)
        self.tail = end
        if self.head is None:
            self.head = self.tail
    
    def is_empty(self):
        return self.head == None
    
    def peek(self):
        if not self.is_empty():
            return self.head.get_value()
        else:
            raise AssertionError("cannot peek at empty queue")