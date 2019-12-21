def func2(H, p, d_type, G):
    p.append(H)
    neighbors = {node:[] for node in p}
    edges = {} 
    mst = []
    for node in p:
        for v in G.neighboors[node]:
            if v in p:
                neighbors[node].append(v)
    visited = {node : False for node in p}
    u = H
    visited[H] = True
    while(all(visited.values()) == False):
        for v in neighbors[u]:
            edges[(u, v)] = G.weight_edges[(v, u)][d_type] 
        if(len(edges) == 0):
            break
        e = min(edges, key=edges.get)
        
        while(visited[e[0]] == visited[e[1]] == True):
            del edges[e]
            e = min(edges, key=edges.get)
        if(visited[e[0]]):
            visited[e[1]] = True
            u = e[1]
        elif(visited[e[1]]):
            visited[e[0]] = True
            u = e[0]           
        mst.append(e)
        del edges[e]    
    if all(visited.values()):
        return mst
    else:
        return -1
