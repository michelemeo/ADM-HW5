import graph as g
import heapq as hp
    

def shortest_path(s, e, d_type, neighboors, edges):
    # shortest_path function is the implementation of the Dijkstra algorithm;
    # to run it in a reasonable time, we use a heap data structure containing tuples which the first element
    # is the 'potential distance' of the unexplored nodes and the second element is the node itself: we need
    # this data structure to evaluate the minimum potential distance in O(const.) time inside the main loop

    distance = {node: 2**32 for node in neighboors}

    # previous is a dictionary that contains the previous node in the path respect to the key node (the default
    # value is -1 because there aren't negative name for the nodes)
    previous = {node: -1 for node in neighboors}
    visited = {node: False for node in neighboors}
    distance[s] = 0
    visited[s] = True
    
    potential = [(distance[s], s)]
    hp.heapify(potential)
    u = s

    while u != e:

        for v in neighboors[u]:
            if visited[v] == False:
                tmp_dist = distance[u] + edges[(u,v)][d_type]

                if tmp_dist < distance[v]:
                    distance[v] = tmp_dist
                    hp.heappush(potential, (distance[v], v))
                    previous[v] = u

        # if the heap is empty, the sequence of nodes are not connected in the graph and we print "Not possible"
        try:      
            u = hp.heappop(potential)[1]
        except:
            print('Not possible')
            
        visited[u] = True


    # this code is necessary to rebuild the path backwards
    path = []
    u = e
    path.append(u)

    while u != s:
        u = previous[u]
        path.append(u)

    # we return the path with the right sequence
    return path[::-1]



def Dijkstra_sequence(s, nodes_list, d_type, neighboors, edges):
    # the function that implement the shortest_path function on all the nodes of the given sequence

    paths = []
    
    for i in range(len(nodes_list)):
        
        path = shortest_path(s, nodes_list[i], d_type, neighboors, edges)
        paths.append(path)
        s = nodes_list[i]
        
    ordered_path = []
    
    for p in paths:
        
        ordered_path += p[1:]
        
    return ordered_path
    
    
    
    
    
    

    










