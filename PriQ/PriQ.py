import random

class PriQ(object):
    '''Binary-Heap based Priority Queue with uniquely named elements, name may \
be any hashable type.  Defaults to min-heap, set maxpq=True for max-heap. \
Public methods: put, get, remove, update, contains, front, get_priority.'''
    
    def __init__(self, maxpq = False):
        self.q =[]          # The priority queue, contains (priority, name) tuples
        self.elements = {}  # Dict of all elements currently in queue, with current index
        self.maxmod = -1 if maxpq else 1   # modify pq to max instead of min

    def __len__(self):
        return len(self.q)
    
    def __str__(self):
        return str(self.q)

    def _propUp(self, index):
        '''Propagate up element to proper place in binary heap'''
        current = index
        while current > 0:
            parent = (current - 1) // 2             # parent node
            # swap with parent until parent <= child (>= for maxPQ)
            if self.q[parent][0] * self.maxmod <= self.q[current][0] * self.maxmod:
                break
            self.elements[self.q[current][1]], self.elements[self.q[parent][1]] = parent, current
            self.q[parent], self.q[current] = self.q[current], self.q[parent]
            current = parent

    def _propDown(self, index):
        '''Propagate down element to proper place in binary heap'''
        if len(self.q) == 1:
            self.elements[self.q[0][1]] = 0         # update index of last element
        current = index
        while current * 2 + 1 < len(self.q):        # node has a child
            left, right = current * 2 + 1, current * 2 + 2
            if right == len(self.q):                # left child only
                if self.q[current][0] * self.maxmod >= self.q[left][0] * self.maxmod:
                    # swap with left child and update elements dict
                    self.elements[self.q[current][1]], self.elements[self.q[left][1]] = left, current
                    self.q[current], self.q[left] = self.q[left], self.q[current]
                break
            if self.maxmod == 1:    # min PQ
                minChild = left if self.q[left] <= self.q[right] else right
                if self.q[current] <= self.q[minChild]: # swap with lowest priority child as needed
                    break
                self.elements[self.q[current][1]], self.elements[self.q[minChild][1]] = minChild, current
                self.q[current], self.q[minChild] = self.q[minChild], self.q[current]
                current = minChild
            else:                   # max PQ
                maxChild = left if self.q[left] >= self.q[right] else right
                if self.q[current] >= self.q[maxChild]: # swap with highest priority child as needed
                    break
                self.elements[self.q[current][1]], self.elements[self.q[maxChild][1]] = maxChild, current
                self.q[current], self.q[maxChild] = self.q[maxChild], self.q[current]
                current = maxChild

    def put(self, name, priority):
        '''Add named element to priorty queue and place in binary heap'''
        if self.contains(name): return ValueError(name)
        self.q.append((priority, name))
        self.elements[name] = len(self.q) - 1
        self._propUp(self.elements[name])

    def front(self):
        '''Element at front of queue'''
        return self.q[0]

    def get_priority(self, name):
        '''Current priority of named element'''
        return self.q[self.elements[name]][0]

    def get(self):
        '''Return element at front of queue and re-heapify queue'''
        if not self.q: 
            return False # empty queue
        result = self.q[0]
        del(self.elements[result[1]])
        if len(self.q) > 1:
            self.q[0] = self.q.pop()
            self._propDown(0)
        else:
            self.q = []
            self.elements = {}
        return result

    def update(self, name, priority):
        '''Change priority of named element and re-heapify'''
        if not self.contains(name): return ValueError(name)
        index = self.elements[name]
        old_priority = self.q[index][0]
        self.q[index] = (priority, name)
        if priority * self.maxmod < old_priority * self.maxmod:
            self._propUp(index)
        if priority * self.maxmod > old_priority * self.maxmod:
            self._propDown(index)

    def contains(self, name):
        '''True if name currently exists in the queue'''
        return (name in self.elements)

    def remove(self, name):
        '''Remove named element and re-heapify'''
        if not self.contains(name): return ValueError(name)
        index = self.elements[name]
        old_priority = self.q[index][0]
        del(self.elements[name])
        if len(self.q) > 1:
            self.q[index] = self.q.pop()    # replace with last item in queue
            self.elements[self.q[index][1]] = index
            # re-heapify
            if self.q[index][0] * self.maxmod < old_priority * self.maxmod:
                self._propUp(index)         
            elif self.q[index][0] * self.maxmod > old_priority * self.maxmod:
                self._propDown(index)
        else:
            self.q = []

###############################################################################
# Following are examples, including Dijkstra's shortest path
###############################################################################

if __name__ == "__main__":
    # Sequential letter names with random integer weights (demonstration)
    pq = PriQ()
    name = 'a'
    for _ in range(26):
        pq.put(name, random.randint(1,99))
        name = chr(ord(name) + 1)
    print("Initial: ['a'-'z' = randint(1,99)]\n", pq, "\nLength: ", len(pq))
    print("Priority of 'a':", pq.get_priority('a'))
    print("Front:", pq.front())
    pq.put('a', 17) # testing for duplicate put
    pq.update('a', 1)
    pq.update('b', 99)
    print("After updating 'a' to 1 and 'b' to 99:\n", pq)
    pq.remove('c')
    print("After removing 'c':\n", pq)
    print("Contains 'c'?", pq.contains('c'))
    print("Get elements until empty:")
    while pq:
        print(pq.get(), "contains 'd'?", pq.contains('d'))

    '''
    # Max-heap priority queue with random float weights and integer names
    pq = PriQ(True)
    for i in range(20):
        pq.put(i, random.random())
    print("['1'-'20' = random()]:\n", pq)
    while pq: print(pq.get())
    '''

    # Dijkstra's shortest path algorithm example
    def dsp(G, s):
        '''Dijkstra's shortest path algorithm.  Input: weighted graph G, an\
    adjacency list mapping each named node to it's neighbors with a {name: weight}\
    dict, and s, the name of the starting node.  Outputs a mapping for each node\
    to a tuple of (weight of shortest path, name of predecessor node).
        '''
        pq = PriQ()
        result = {}
        predecessor = {s: None}
        for key in G.keys():
            pq.put(key, 0 if key == s else float('inf'))
        while pq:
            cur_weight, cur_node = pq.get()
            result[cur_node] = (cur_weight, predecessor[cur_node])
            for adj in G[cur_node]:     # for neighboring nodes
                # update weight from starting node if less than previous paths
                if adj not in result:
                    if pq.get_priority(adj) > cur_weight + G[cur_node][adj]:
                        pq.update(adj, cur_weight + G[cur_node][adj])
                        predecessor[adj] = cur_node
        return result

    G = {
        'a': {'b': 2, 'f': 6, 'c': 1},
        'b': {'a': 2, 'd': 6, 'f': 3, 'g': 4},
        'c': {'a': 1, 'f': 2, 'g': 3, 'e': 5},
        'd': {'b': 6, 'f': 2, 'g': 1, 'h': 2},
        'e': {'c': 5, 'f': 4, 'g': 2, 'h': 3},
        'f': {'a': 6, 'b': 3, 'd': 2, 'g': 7, 'e': 4, 'c': 2},
        'g': {'f': 7, 'b': 4, 'd': 1, 'h': 5, 'e': 2, 'c': 3},
        'h': {'d': 2, 'g': 5, 'e': 3}
        }
    print(
    '''
        B  6  D
      2 3 2 4 1 2
    A 6 F  7  G 5 H
      1 2 3 4 2 3
        C  5  E
    ''')
    print("\nCalculating shortest paths with Dijkstra's algorithm...")
    print("Shortest paths from 'a':", dsp(G, 'a'))
    print("Shortest paths from 'd':", dsp(G, 'd'))