class MaxHeap(object):
    ''' a max heap, maintaining the max heap invariants:
    (1) maximum value is at the root 
    (2) for every note N, N.left.value and N.right.value are less than N.value '''
    
    def __init__(self):
        self.heap_list = [0]
        self.heap_size = 0      ### N.B important to maintain the offset between list length and heap size for traversal by division
        
        
    def insert(self, a):
        ''' insert the value [a] into the heap '''
        
        self.heap_list.append(a)
        self.heap_size += 1
        self._pushup(self.heap_size)
        
    def extract_max(self):
        ''' extract the max and adjust the heap so the 
        invariants are maintained '''
        
        max_val = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.heap_size]
        self.heap_list.pop()
        self.heap_size -= 1
        self._pushdown(1)
        return max_val    
            
    def _pushup(self,pos):
        ''' adjust the heap after insertion so that the value at position [pos] 
        maintains the heap invariant.'''
        index = pos
        while index // 2 > 0:
            parent = index // 2
            if self.heap_list[index] > self.heap_list[parent]:
                temp = self.heap_list[parent]
                self.heap_list[parent] = self.heap_list[index]
                self.heap_list[index] = temp
            index = parent
        
    def _pushdown(self,index):
        ''' adjust the heap after deletion by replacing the vacant root
        with the smallest value, and then pushing it down the heap. '''
       
        while index * 2 <= self.heap_size:
            swap_pos = self._get_max_child(index)
            if self.heap_list[index] < self.heap_list[swap_pos]:
                temp = self.heap_list[index]
                self.heap_list[index] = self.heap_list[swap_pos]
                self.heap_list[swap_pos] = temp
            index = swap_pos
                     
    
    def _get_max_child(self, pos):
        ''' return the position of the child of node at pos that is storing 
        the largest value'''
        if pos * 2 + 1 > self.heap_size:
            # tree is not complete but not full
            return pos * 2
        else:
            if self.heap_list[pos * 2] > self.heap_list[pos * 2 + 1]:
                return pos * 2
            else:
                return pos * 2 + 1
        