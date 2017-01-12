from node import Node

class Queue:
    
    def __init__(self):
        head = None
        tail = None
    
    def remove():
        if not is_empty():
            t = head.get_value()
            head = head.get_next()
            if head is None:
                tail = None
            return t
        else:
            raise AssertionError("cannot pop empty queue")
    
    def add(item):
        end = Node(v=item)
        if tail is not None:
            tail.set_next(end)
        tail = end
        if head is None:
            head = tail
    
    def is_empty():
        return head == None
    
    def peek():
        if not is_empty():
            return head.get_value()
        else:
            raise AssertionError("cannot peek at empty queue")