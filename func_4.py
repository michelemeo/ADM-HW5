import heapq as hp
from pyproj import Proj, transform
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, MultiLine
from bokeh.io import output_notebook, show, reset_output
from bokeh.plotting import figure

def shortest_path(s, e, d_type, G):

    distance = {node: 2**32 for node in G.neighboors} #each node's distance from s
    previous = {node: -1 for node in G.neighboors} #from which node they reach s
    visited = {node: False for node in G.neighboors} 
    distance[s] = 0
    visited[s] = True
    
    potential = [(distance[s], s)]
    hp.heapify(potential)
    u = s

    while u not in e: #e is a list of nodes and whenever we find one it's nodes we'll stop looking

        for v in G.neighboors[u]:
            if visited[v] == False:
                tmp_dist = distance[u] + G.weight_edges[(u,v)][d_type]

                if tmp_dist < distance[v]: #if new distance is less update the path
                    distance[v] = tmp_dist
                    hp.heappush(potential, (distance[v], v))
                    previous[v] = u
                
        try:
            u = hp.heappop(potential)[1] #get minimum using heap structure
        except:
            return -1
        visited[u] = True
    path = []
    path.append(u)

    while u != s:  
        path.append(u)
        u = previous[u]
    return path[::-1]

#to find the shortest walk we're going to start from the first node
#and use dijkstra algorithm to find the neart node from the list
#then repeat this process untill no node remains inside the list
def func4(H, to_go, d_type, G):
    path = [H]
    u = H
    while(len(to_go) > 0):
        sp = shortest_path(u, to_go, 'd', G)
        if sp == -1:
            return -1
        else:
            path += sp[:-1]
        u = path[-1]
        to_go.remove(u)
    return path
    


# convert longitude, latitude to mercator coordinates
def create_coordinates(long_arg,lat_arg):
    in_wgs = Proj(init='epsg:4326')
    out_mercator = Proj(init='epsg:3857')
    long, lat = long_arg, lat_arg
    mercator_x, mercator_y = transform(in_wgs, out_mercator, long, lat)
    #print(mercator_x, mercator_y)
    return tuple([mercator_x, mercator_y])

def vis4(result, d_type, G):
    if result == -1: #----- if graph is not connected!
        print("Not possible!")
    else:
        indices = set() # to store nodes
        start = [] # to store start and end of each edge
        end = []
        start.append(result[0])
        for item in result[1:]: #add nodes
            indices.add(item)
            start.append(item)
            end.append(item)
        start = start[:-1]
        indices = list(indices)
        x = []
        y = []
        for node in indices:  #convert longitude, latitude to mercator coordinates
            xy = create_coordinates(G.coord_nodes[node][0]/1000000, G.coord_nodes[node][1]/1000000)
            x.append(xy[0])
            y.append(xy[1])
        
        tile_provider = get_provider(Vendors.CARTODBPOSITRON)
        #output_notebook()
        # range bounds supplied in web mercator coordinates
        m = figure(plot_width=800, 
                   plot_height=400,
                   x_range=(min(x)-200, max(x)+200), #span of the map
                   y_range=(min(y)-200, max(y)+200),
                   x_axis_type='mercator', 
                   y_axis_type='mercator')

        m.add_tile(tile_provider)

        graph = GraphRenderer() #initializing the graph
        graph.node_renderer.data_source.add(indices, 'index')
        edge_color = 'black'
        if d_type == 'd':
            edge_color = 'blue'
        elif d_type == 't':
            edge_color = 'yellow'
        elif d_type == 'n':
            edge_color = 'green'
        graph.node_renderer.glyph = Oval(height=20, width=20, fill_color='red')
        graph.edge_renderer.data_source.data = dict( start = start, end = end)
        graph.edge_renderer.glyph = MultiLine(line_color=edge_color, line_alpha=0.8, line_width=2)

        graph_layout = dict(zip(indices, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        m.renderers.append(graph) #assigning the graph to the map
        show(m)
