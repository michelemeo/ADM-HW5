from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, MultiLine
from bokeh.io import output_notebook, show, reset_output
from bokeh.plotting import figure
from pyproj import Proj, transform

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
        try:
            e = min(edges, key=edges.get)
        except:
            return -1
        
        while(visited[e[0]] == visited[e[1]] == True):
            del edges[e]
            try:
                e = min(edges, key=edges.get)
            except:
                return -1
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

# convert longitude, latitude to mercator coordinates

def create_coordinates(long_arg,lat_arg):
    in_wgs = Proj(init='epsg:4326')
    out_mercator = Proj(init='epsg:3857')
    long, lat = long_arg, lat_arg
    mercator_x, mercator_y = transform(in_wgs, out_mercator, long, lat)
    #print(mercator_x, mercator_y)
    return tuple([mercator_x, mercator_y])

def vis2(result, d_type, G):
    if result == -1: #----- if graph is not connected!
        print("Not connected!")
    else:
        indices = set() # to store nodes
        start = [] # to store start and enf of each edge
        end = []
        edge_color = [] #to recognize output from other edges
        for item in result: #add nodes
            indices.add(item[0])
            indices.add(item[1])
        indices = list(indices)
        for node in indices: #add edges
            for v in G.neighboors[node]:
                if v in indices:
                    start.append(node)
                    end.append(v)
                    if ((node, v) in result) or ((v, node) in result): #if it's in output give it a color
                        if d_type == 't':
                            edge_color.append('red')
                        elif d_type == 'd':
                            edge_color.append('blue')
                        else:
                            edge_color.append('green')
                    else:
                        edge_color.append('black') #else it would be black
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
        graph.node_renderer.glyph = Oval(height=20, width=20, fill_color='black')
        graph.edge_renderer.data_source.data = dict( start = start, end = end)
        graph.edge_renderer.data_source.add(edge_color, 'color')
        graph.edge_renderer.glyph = MultiLine(line_color='color', line_alpha=0.8, line_width=2)

        graph_layout = dict(zip(indices, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        m.renderers.append(graph) #assigning the graph to the map
        show(m)

