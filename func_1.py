import graph as g

def neighborhood_BFS(v, d_type, thr, neighboors, edges):
    # we implement the BFS algorithm with some modifications to take in count the distances of all the
    # visited nodes from the starting node v

    # we use a queue that is implemented from scratch in graph.py
    q = g.Queue()
    visited = {node: False for node in neighboors}
    distance = {node: 0 for node in neighboors}
    

    q.enqueue(v)
    visited[v] = True
        

    while q.isEmpty() == False:
        v = q.dequeue()

        for u in neighboors[v]:
            # if the distance is bigger than the threshold, we must skip this iteration
            if distance[v]+edges[(v,u)][d_type] > thr:
                continue

            # if we already visited the node but the distance from v is smaller than the threshold, we
            # need anyway to update it and to reinsert u in queue
            elif visited[u] == True and distance[v]+edges[(v,u)][d_type] < distance[u]:
                q.enqueue(u)
                distance[u] = distance[v]+edges[(v,u)][d_type]
                continue

            # if the node is visited and has passed the previous if, we can skip to the next iteration
            elif visited[u] == True:
                continue

            else:                
                q.enqueue(u)
                visited[u] = True
                distance[u] = distance[v] + edges[(v,u)][d_type]

    neighborhood = [node for node in visited if visited[node] == True]
    return neighborhood