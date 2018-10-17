import heapq
from max_heap import MaxHeap

### test a heap
def test_simple_list(l):
    maxheap = MaxHeap()
    for item in l:
        maxheap.insert(item)
    heapq._heapify_max(l)
    
    length = len(l)
    for j in range(length):
        my_max = maxheap.extract_max()
        hq_max = heapq._heappop_max(l)
        assert(my_max == hq_max)
    return True


if __name__ == "__main__":
    simple_list = [21,1,45,78,3,5]
    test_simple_list(simple_list)