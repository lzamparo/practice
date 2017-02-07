### merge-sort implementation in python
import numpy as np
import timeit
    
def merge_sort_rec(my_array):
    if len(my_array) <= 1:
        return my_array
    middle = len(my_array) // 2
    left = merge_sort_rec(my_array[:middle])
    right = merge_sort_rec(my_array[middle:])
    return rec_merge(left,right)

def merge_sort_iterative(my_array):
    if len(my_array) <= 1:
        return my_array
    middle = len(my_array) // 2
    left = merge_sort_iterative(my_array[:middle])
    right = merge_sort_iterative(my_array[middle:])
    return iterative_merge(left,right)    

def rec_merge(left, right):
    ''' Repeatedly merge sorted sublists to produce a larger sorted list  
    n.b lists of length 1 is sorted.
    ''' 
    if not left:
        return right    
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + rec_merge(left[1:], right)
    return [right[0]] + rec_merge(left, right[1:])
    
def iterative_merge(left, right):
    ''' Repeatedly merge sorted sublists left, right '''
    i,j = 0,0
    merged = []
    while i < len(left) and j < len(right):
        # go through the arrays, performing a running insertion-sort
        
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        
        else:
            merged.append(right[j])
            j += 1
        
        # once we exhaust one array, just append each element of the other (since both are sorted, to save time.)
        if i == len(left):
            merged.extend(right[j:])
            break
        
        if j == len(right):
            merged.extend(left[i:])
            break
            
    return merged


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped
        
if __name__ == "__main__":
    n = np.random.randint(100)
    unsorted = [i for i in range(n)]
    np.random.shuffle(unsorted)
    
    recursive_wrapped = wrapper(merge_sort_rec, unsorted)
    print("1000 average timed iterations of recursive mergesort : ", timeit.timeit(recursive_wrapped, number=1000))      
    
    iterative_wrapped = wrapper(merge_sort_iterative, unsorted)
    print("1000 average timed iterations of iterative mergesort : ", timeit.timeit(iterative_wrapped, number=1000))
    
        
    
    