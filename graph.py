# the class to build the graph, as already described in main.py
class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.neighboors = {}
        self.weight_edges = {}
        self.coord_nodes = {}
        
        
    def add_node(self, node):
        self.nodes.add(node)
        
        
    def add_edge(self, edge):
        self.edges.add(edge)


    def direct_neighboors(self):
        if len(self.neighboors) == 0:
            self.neighboors = {node: [] for node in self.nodes}

        for item in self.edges:
               self.neighboors[item[0]].append(item[1])
    
    
    def weighted_edges(self, data, type_of_distance):
        if len(self.weight_edges) == 0:
            self.weight_edges = {edge: {} for edge in self.edges}
        
        for item in data:
             self.weight_edges[(item[0], item[1])][type_of_distance] = item[2]
                
    
    def add_network_distance(self):
        for key in self.weight_edges:
             self.weight_edges[key]['n'] = 1
                
    
    def coordinate_nodes(self, data):
        if len(self.coord_nodes) == 0:
            self.coord_nodes = {node: [] for node in self.nodes}

        for item in data:
               self.coord_nodes[item[0]].append(item[1])
               self.coord_nodes[item[0]].append(item[2]) 
            

# implementation from scratch of the queue data structure, using lists
class Queue:
    
    def __init__(self):
        self.queue = []
        
        
    def enqueue(self, x):
        self.queue.append(x)
        
        
    def dequeue(self):
        return self.queue.pop(0)
        
        
    def front(self):
        return self.queue[0]
    
    
    def size(self):
        return len(self.queue)
    
    
    def isEmpty(self):
        if self.size() == 0:
            return True
        else:
            return False
        
        
        
        
        
        
        
        
        
        
        
        
        