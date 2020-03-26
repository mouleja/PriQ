# This is mostly of test of my PriQ module
from PriQ import PriQ

# Dijkstra's shortest path algorithm example
def dsp(G, s):
    '''Dijkstra's shortest path algorithm.  Input: weighted graph G, an \
adjacency list mapping each named node to it's neighbors with a {name: weight} \
dict, and s, the name of the starting node.  Outputs a mapping for each node \
to a tuple of (weight of shortest path, name of predecessor node).
    '''
    pq = PriQ.PriQ()
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