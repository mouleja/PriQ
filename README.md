# PriQ
## Python priority queue class with features not in default implementation

## Binary-Heap based Priority Queue with uniquely named elements, name may be any hashable type.
### Defaults to min-heap, set maxpq=True for max-heap.

### Public methods: put, get, remove, update, contains, front, get_priority.

put - Add named element to priorty queue and place in binary heap

front - Element at front of queue

get_priority - Current priority of named element

get - Return element at front of queue and re-heapify queue

update  - Change priority of named element and re-heapify

contains - True if name currently exists in the queue

remove - Remove named element and re-heapify

## Contains examples, including Dijkstra's shortest path algo
