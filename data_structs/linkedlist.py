class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        
    # Insert at tail    
    def insert(self, node):
        if (self.head == None):
            self.head = node
            self.tail = node
        else:
            temp = self.head
            while (temp.get_next() != None):
                temp = temp.get_next()
            temp.set_next(node)
            node.set_prev(temp)
            self.tail = node
            
    # Reverse the list
    def reverse(self):
        temp = self.tail
        self.head = temp

        while (temp.get_prev() != None):
            new_next = Node(None,temp.get_prev(),0)
            temp.set_prev(temp.get_next())
            temp.set_next(new_next.get_next())
            temp = new_next.get_next()
        self.tail = temp
        self.tail.set_next(None)
    
    # Print a string representation of the list
    # Causes an infinite loop after reversing?
    def print_list(self):
        if (self.head == None):
            print "[]"
        else:
            der_string = "["
            temp = self.head
            while (temp != None):
                der_string += str(temp.get_value())
                if (temp.get_next() != None):
                    der_string += ","
                temp = temp.get_next()
            der_string += "]"
            print der_string
            
            