import numpy as np
import pandas as pd
import csv
import igraph as ig
import plotly.graph_objs as go
import plotly.offline as pyo

def csv2graph(treecsv):
    '''
    creates igraph object from csv file
    '''
    G = ig.Graph(directed = True)
    #read csv file
    with open (treecsv, 'rt') as file:
        csvreader = csv.reader(file, delimiter=',')
        children = []
        nodes = []
        for row in csvreader:
            children.append(row) #list of lists
            nodes.extend(row) #just list
        #add nodes from the list
        G.add_vertices(list(set(nodes)))
        #add edges for each children node in csv file row
        for row in children:
            row = list(filter(None, row))
            if len(row) > 1:
                child = row[0]
            for parent in row[1:]:
                G.add_edge(parent, child)
    return G

def add_attributes(G, attr_file):
    '''
    add attributes from csv file to graph nodes
    csv file columns: ['Path', 'Name', 'Size', 'Type']
    '''
    df = pd.read_csv(attr_file)
    #add graph property with root directory name
    G['root_dir'] = df['Path'][0]

    #default nodes color for non-grouped files
    df['Color'] = 'magenta'
    #groups by file type
    code = ['.R', '.pl', '.c','.py','.js']#files with code
    data = ['.xlsx', '.xls', '.txt','.tsv','.csv']#ascii data
    databin = ['.gz', '.RData','.Rdata']#binary data files
    #color different file types
    df.loc[df['Type'].isin(code),['Color']] = 'red'
    df.loc[df['Type'].isin(data),['Color']] = 'blue'
    df.loc[df['Type'].isin(databin),['Color']] = 'green'
    df.loc[df['Size'].isnull(),['Color']] = 'black'#folders
    #replace NaN for size with zeros
    df['Size'].fillna(0, inplace=True)
    #iterate over nodes and add attributes
    size_scale = 1e+06#rescale file size to Mb
    #iterate over nodes and add color and size
    for i in range(G.vcount()):
        elname = G.vs[i]['name']
        G.vs[i]['color'] = df.loc[df['Path'] == elname,'Color'].values[0]
        G.vs[i]['size'] = df.loc[df['Path'] == elname,'Size'].values[0]/size_scale
        G.vs[i]['element'] = G.vs[i]['name'].split('/')[-1]
        G.vs[i]['label'] = f"{G.vs[i]['element']}: {round(G.vs[i]['size'], 2)}Mb"
    return G

def graph2html(G, gstyle, fname):
    #setting size for nodes
    size_gr = {'small':10,'scaled':10,'dirs':20}
    nsizes = []
    for nsize in G.vs['size']:
        if nsize == 0.0:
            nsizes.append(size_gr['dirs'])
        elif nsize > 5:
            nsizes.append(size_gr['scaled']*np.log(nsize))
        else:
            nsizes.append(size_gr['small'])

    #create layout of coordinates (see igraph docs for options)
    root_index = G.vs.find(G['root_dir']).index
    glayout = G.layout_reingold_tilford(mode='all', root = [root_index])
    #inverse coordinates to flip folder tree
    def flipax(ax):
        nax = [-1*i for i in ax if i != None]
        return nax

    #ploting edges
    edge_trace = go.Scatter(x = [],
                    y = [],
                    mode = 'lines',
                    line = dict(
                            color = 'rgb(210,210,210)',
                            width = 3),
                    hoverinfo = 'none'
                )
    #list of edges converted to tuples
    nedges = [edge.tuple for edge in G.es]
    #dots for line coordinates: [x0, x1, attribute = None]
    for e in nedges:
        edge_trace['x'] += [glayout[e[0]][0], glayout[e[1]][0], None]
        edge_trace['y'] += [glayout[e[0]][1], glayout[e[1]][1], None]
    #invert edges coordinates
    edge_trace['x'] = flipax(edge_trace['x'])
    edge_trace['y'] = flipax(edge_trace['y'])

    #plotting nodes
    node_trace = go.Scatter(x = [],
                    y = [],
                    mode = 'markers',
                    name = G['root_dir'],
                    marker = dict(symbol = 'circle-dot',
                                            size = nsizes,
                                            color = G.vs['color'],
                                            line = dict(
                                                color='rgb(50,50,50)',
                                                width = 1),
                                            ),
                    text = G.vs['label'],
                    hoverinfo = 'text'
                    )

    #Nodes coordinates (x & y)
    node_trace['x'] = flipax([glayout[k][0] for k in range(G.vcount())])
    node_trace['y'] = flipax([glayout[k][1] for k in range(G.vcount())])

    #axis parameters for layout
    axis = dict(showline = False, #hide axis line
        zeroline = False, #hide zeroline
        showgrid = False, #hide grid
        showticklabels = False, # hide tick showticklabels
        title = '' #hide title
            )

    #figure layout object
    layout = go.Layout(title = f"Content of {G['root_dir']}",
            font = dict(size=12),
            showlegend = False,
            autosize = False,
            width = 1500, #dimensions of the plot
            height = 1000, #dimensions of the plot
            xaxis = axis,
            yaxis = axis,
            margin = dict(l = 40, r = 40, b = 40, t = 40),
            hovermode = 'closest',

            annotations = [
                dict(
                showarrow = False,
                text = 'legend',
                xref = 'paper',
                yref = 'paper',
                x = 0,
                y = -0.1,
                xanchor='left',
                yanchor='bottom',
                font=dict(size=14)
                )
            ]
            )

    data = [edge_trace, node_trace]
    #generate figure
    fig = go.Figure(data = data, layout = layout)
    #generate .html file
    repofname = f"{G['root_dir']}-{gstyle}{fname}"
    pyo.plot(fig, filename = repofname)

    return [edge_trace, node_trace]

if __name__ == '__main__':
    #directory tree: 'rootdir, subdir1, subdir2'
    treefile = 'DirectoryNodes_wPaths.csv'
    #attributes file: ['Path', 'Name', 'Size', 'Type']
    attributes = 'NodeTypes_wPaths.csv'
    #graph layout (not used)
    gstyle = 'rt'
    fname = '-ig.html'
    G = add_attributes(csv2graph(treefile), attributes)
    Gout = graph2html(G, gstyle, fname)
