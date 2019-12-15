import graph as g

def neighborhood_BFS(v, d_type, thr, neighboors, edges):

    q = g.Queue()
    visited = {node: False for node in neighboors}
    distance = {node: 0 for node in neighboors}
    

    q.enqueue(v)
    visited[v] = True
        

    while q.isEmpty() == False:
        v = q.dequeue()

        for u in neighboors[v]:
            if distance[v]+edges[(v,u)][d_type] >= thr:
                continue
            elif visited[u] == True and distance[v]+edges[(v,u)][d_type] < distance[u]:
                q.enqueue(u)
                distance[u] = distance[v]+edges[(v,u)][d_type]
                continue
            elif visited[u] == True:
                continue
            else:                
                q.enqueue(u)
                visited[u] = True
                distance[u] = distance[v] + edges[(v,u)][d_type]

    neighborhood = [node for node in visited if visited[node] == True]
    return neighborhood