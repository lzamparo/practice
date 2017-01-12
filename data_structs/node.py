class Node:
    def __init__(self,p=None,n=None,v=0):
        self.next = n
        self.prev = p
        self.value = v
        
    def get_next(self):
        return self.next
    
    def get_prev(self):
        return self.prev
    
    def get_value(self):
        return self.value
    
    def set_next(self,node):
        self.next = node
        
    def set_prev(self,node):
        self.prev = node
        
    def set_value(self,val):
        self.value = val
        