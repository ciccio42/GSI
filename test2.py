import networkx as nx
import random
#import matplotlib.pyplot as plt

def generate_numbered_bidirectional_grid_graph(rows, cols, node_label_range, edge_label):
    # Create an empty graph
    G = nx.DiGraph()

    # Add nodes with random labels
    for i in range(rows * cols):
        G.add_node(i, label=random.randint(1, node_label_range))

    # Add edges and make them bidirectional
    for i in range(rows):
        for j in range(cols):
            current = i * cols + j
            if j < cols - 1:  # Horizontal edge
                right = current + 1
                G.add_edge(current, right, label=edge_label)
                G.add_edge(right, current, label=edge_label)
            if i < rows - 1:  # Vertical edge
                down = current + cols
                G.add_edge(current, down, label=edge_label)
                G.add_edge(down, current, label=edge_label)

    return G

'''
# Parameters
rows = 10
cols = 10
node_label_range = 1
edge_label = 1

# Generate the bidirectional grid graph
G = generate_numbered_bidirectional_grid_graph(rows, cols, node_label_range, edge_label)

# Draw the graph
pos = {i: (i % cols, -i // cols) for i in G.nodes()}
node_labels = nx.get_node_attributes(G, 'label')
edge_labels = nx.get_edge_attributes(G, 'label')

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
#nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')

plt.show()

# Print some basic information about the graph
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())
'''