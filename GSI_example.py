import timeit
import networkx as nx
from GSI import initGPU, createGraph, findIsomorphism, printMappings, nxGraph, printGraph
from networkx.algorithms import isomorphism
import test

# Initialize GPU
initGPU(dev=0)
print()

'''
# Create two sample graphs using raw data
node_ids1 = [0, 1, 2]
node_labels1 = [1, 2, 3]
edge_ids1 = [(0, 1), (1, 2)]
edge_labels1 = [10, 20]

node_ids2 = [0, 1, 2]
node_labels2 = [1, 2, 3]
edge_ids2 = [(0, 1), (1, 2)]
edge_labels2 = [10, 20]

# Create custom Graph objects
graph1 = createGraph(node_ids1, node_labels1, edge_ids1, edge_labels1, column_oriented=False)
graph2 = createGraph(node_ids2, node_labels2, edge_ids2, edge_labels2, column_oriented=True)

# Profile the time taken to find isomorphisms between the two graphs using timeit
execution_time_custom = timeit.timeit(
    stmt='findIsomorphism(graph1, graph2)',
    setup='from __main__ import findIsomorphism, graph1, graph2',
    number=1
)

# Find isomorphisms between the two graphs
is_isomorphic_custom, mappings_custom = findIsomorphism(graph1, graph2)

# Print the result
if is_isomorphic_custom:
    print("Isomorphism found!")
    printMappings(mappings_custom)
else:
    print("No isomorphism found.")

print(f"Time taken to find isomorphisms with custom method: {execution_time_custom:.6f} seconds")
'''
'''
# Demonstration using NetworkX graph
# Create a NetworkX graph
query_nx = nx.Graph()
query_nx.add_nodes_from([(i, {'label': i % 3 + 1}) for i in range(25)])
query_edges = [(i, (i+1) % 25, {'label': i % 5 + 1}) for i in range(25)]
query_nx.add_edges_from(query_edges)

# Create a larger data graph using NetworkX
data_nx = nx.Graph()
data_nx.add_nodes_from([(i, {'label': i % 3 + 1}) for i in range(100)])
data_edges = [(i, (i+1) % 100, {'label': i % 5 + 1}) for i in range(100)]
data_edges += [(i, (i+2) % 100, {'label': i % 5 + 1}) for i in range(50)]
data_nx.add_edges_from(data_edges)
'''

# Data graph
data_nx = test.generate_numbered_bidirectional_grid_graph(10, 10, 1, 1)


# Query graph
query_nx = test.generate_numbered_bidirectional_grid_graph(5, 4, 1, 1)


# Convert NetworkX graphs to custom Graph objects
query_graph = nxGraph(query_nx, column_oriented=False)
data_graph = nxGraph(data_nx, column_oriented=True)

printGraph(data_graph)

quit()

# Profile the time taken to find isomorphisms between NetworkX-based custom graphs using timeit
execution_time_custom_nx = timeit.timeit(
    stmt='findIsomorphism(query_graph, data_graph)',
    setup='from __main__ import findIsomorphism, query_graph, data_graph',
    number=1
)

# Find isomorphisms between NetworkX-based custom graphs
is_isomorphic_custom_nx, mappings_custom_nx = findIsomorphism(query_graph, data_graph)

# Print the result
if is_isomorphic_custom_nx:
    print("Isomorphism found between NetworkX graphs using custom method!")
    print(mappings_custom_nx[0])
    #printMappings(mappings_custom_nx)
else:
    print("No isomorphism found between NetworkX graphs using custom method.")

print(f"Time taken to find isomorphisms between NetworkX graphs with custom method: {execution_time_custom_nx:.6f} seconds")

# Profile the time taken to find isomorphisms using NetworkX's built-in method on the larger graphs
execution_time_nx = timeit.timeit(
    stmt='isomorphism.GraphMatcher(data_nx, query_nx).subgraph_is_isomorphic()',
    #setup='import networkx as nx; from networkx.algorithms import isomorphism; import test;data_nx=test.generate_numbered_bidirectional_grid_graph(10, 10, 2, 1);query_nx=test.generate_numbered_bidirectional_grid_graph(4, 5, 2, 1)',
    setup='from __main__ import query_nx, data_nx; from networkx import isomorphism',
    number=1
)

# Find isomorphisms using NetworkX's built-in method
GM = isomorphism.GraphMatcher(data_nx, query_nx)
is_isomorphic_nx = GM.subgraph_is_isomorphic()

# Print the result
if is_isomorphic_nx:
    print("Isomorphism found between NetworkX graphs using NetworkX method!")
else:
    print("No isomorphism found between NetworkX graphs using NetworkX method.")

print(f"Time taken to find isomorphisms between NetworkX graphs with NetworkX method: {execution_time_nx:.6f} seconds")