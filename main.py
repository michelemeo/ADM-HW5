import matplotlib.pyplot as plt
import time
import networkx as nx

# we import the graph.py modules that contains a class to build the graph and other utilities
import graph as g

# we import all the functionalities that we have implemented
import func_1 as f1
import func_2 as f2
import func_3 as f3
import func_4 as f4


print('\nThe program provides users with information about roads in California and Nevada and has 4 functionalities:\n'
      '1 - FIND THE NEIGHBOORS!: it returns the set of nodes at distance <= d from v (starting node), corresponding to v’s neighborhood;\n'
      '2 - FIND THE SMARTEST NETWORK!: it returns the set of roads (edges) that enable the user to visit all the places;\n'
      '3 - SHORTEST ORDERED ROUTE: it returns the shortest walk that goes from a starting node to another node visiting in order the nodes contained in a list;\n'
      '4 - SHORTEST ROUTE: it returns the shortest walk that goes from a starting node to another node visiting all the nodes in list in any order.\n\n'
      '...loading the program...\n')

# we import the data and save it in lists
data_d = []
data_t = []
data_coor = []

with open('USA-road-d.CAL.gr', 'r') as file:
    raw_data_d = file.readlines()

with open('USA-road-t.CAL.gr', 'r') as file:
    raw_data_t = file.readlines()

with open('USA-road-d.CAL.co', 'r') as file:
    raw_data_coor = file.readlines()

for row in range(7, len(raw_data_d)):
    data_d.append(list(map(int, raw_data_d[row][2:-1].split())))

for row in range(7, len(raw_data_d)):
    data_t.append(list(map(int, raw_data_t[row][2:-1].split())))

for row in range(7, len(raw_data_coor)):
    data_coor.append(list(map(int, raw_data_coor[row][2:-1].split())))


# we build the graph with the following main structure:
# - G.neighboors: a dictionary containing nodes as keys and a list of neighbors for each node as a value
# - G.weight_edges: a dictionary containing all edges as keys associated with a dictionary containing all distances as a value
# - G.coor_nodes: a dictionary containing all nodes as keys and geographic coordinates as values
# (see graph.py for details)
G = g.Graph()

# we add all the nodes and all the edges to two sets which we then convert into lists
for item in data_d:
    G.add_node(item[0])
    G.add_edge((item[0], item[1]))

G.nodes = list(G.nodes)
G.edges = list(G.edges)

# in order, we build the G.neighboors dictionary... we build the G.weight_edges dictionary and we add to it
# all the type of distances (spatial, temporal and network)... we build the G.coord_nodes dictionary
# (read the following functions in graph.py)
G.direct_neighboors()
G.weighted_edges(data_d, type_of_distance='d')
G.weighted_edges(data_t, type_of_distance='t')
G.add_network_distance()
G.coordinate_nodes(data_coor)

print('Which functionality do you want to start? Enter a number (1, 2, 3 or 4)...')
f = int(input())

if f == 1:

    print('Enter in the order the starting node (v), the distance type ("d", "t" or "n"), a distance threshold (d):')
    inputs = list(map(str, input().split()))
    v, type, d = int(inputs[0]), inputs[1], int(inputs[2])

    # we run functionality 1 (read func_1.py)
    neig_nodes = f1.neighborhood_BFS(v, type, d, G.neighboors, G.weight_edges)

    s_graph = nx.Graph()

    edges = []

    for node in neig_nodes[1:]:
        s_graph.add_node(node, pos=(G.coord_nodes[node][0], G.coord_nodes[node][1]), color='black', size=3,
                         label='V neighboors')

    s_graph.add_node(neig_nodes[0], pos=(G.coord_nodes[neig_nodes[0]][0], G.coord_nodes[neig_nodes[0]][1]),
                     color='red', size=60, label='node V')

    if type=='d': c = 'green'
    elif type=='t': c = 'blue'
    elif type=='n': c ='purple'

    for node in neig_nodes:
        for neig in G.neighboors[node]:
            if neig in neig_nodes:
                s_graph.add_edge(node, neig)

    fig = plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(s_graph, nx.get_node_attributes(s_graph, 'pos'),
                           node_color=list(nx.get_node_attributes(s_graph, 'color').values()),
                           node_size=list(nx.get_node_attributes(s_graph, 'size').values()),
                           label='neighboors')
    nx.draw_networkx_edges(s_graph, nx.get_node_attributes(s_graph, 'pos'),
                           edge_color=c, width=0.5, label='edges')
    plt.title('Neighboorhood of V (red node)')
    plt.legend()
    plt.show()
    
elif f == 2:
    
    print('Enter in the order the starting node (v), a sequence of nodes (input format: [n1,n2,n3,..]), the distance type ("d", "t" or "n"):')
    inputs = list(map(str, input().split()))
    v, d_type = int(inputs[0]), inputs[2]
    sequence = list(map(int, inputs[1][1:-1].split(',')))

    # we run functionality 2 (read func_2.py)
    result = f2.func2(v, sequence, d_type, G)
    f2.vis2(result, d_type, G)
    
elif f == 3:

    print('Enter in the order the starting node (v), a sequence of nodes (input format: [n1,n2,n3,..]), the distance type ("d", "t" or "n"):')
    inputs = list(map(str, input().split()))
    v, type = int(inputs[0]), inputs[2]
    sequence = list(map(int, inputs[1][1:-1].split(',')))

    # we run functionality 3 (read func_3.py)
    path = f3.Dijkstra_sequence(v, sequence, type, G.neighboors, G.weight_edges)

    s_graph = nx.Graph()

    s_graph.add_node(v, pos=(G.coord_nodes[v][0], G.coord_nodes[v][1]),
                     color='green', size=100)

    for node in path:
        s_graph.add_node(node, pos=(G.coord_nodes[node][0], G.coord_nodes[node][1]),
                         color='black', size=2)

    s_graph.add_node(path[-1], pos=(G.coord_nodes[path[-1]][0], G.coord_nodes[path[-1]][1]),
                     color='red', size = 80)

    s_graph.add_edge(v, path[0])

    for i in range(len(path)-1):
        s_graph.add_edge(path[i], path[i+1])

    fig = plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(s_graph, nx.get_node_attributes(s_graph, 'pos'),
                           node_color=list(nx.get_node_attributes(s_graph, 'color').values()),
                           node_size=list(nx.get_node_attributes(s_graph, 'size').values()))
    nx.draw_networkx_edges(s_graph, nx.get_node_attributes(s_graph, 'pos'),
                           edge_color='blue', width=1, label='shortest path')

    plt.title('Shortest Route from the green node\n to the red node')
    plt.legend()
    plt.show()

elif f == 4:
    
    print('Enter in the order the starting node (v), a sequence of nodes (input format: [n1,n2,n3,..]), the distance type ("d", "t" or "n"):')
    inputs = list(map(str, input().split()))
    v, d_type = int(inputs[0]), inputs[2]
    sequence = list(map(int, inputs[1][1:-1].split(',')))

    # we run functionality 4 (read func_4.py)
    result = f4.func4(v, sequence, d_type, G)
    f4.vis4(result, d_type, G)
