from datetime import date
import dash
from dash import dcc
from dash import html, Input, Output, State
import plotly.graph_objs as go
import networkx as nx
from colour import Color
from dash.exceptions import PreventUpdate
from requete import Requete, RequeteTwitter, RequeteArxiv
from document import Document, Tweet
from corpus import Corpus

app = dash.Dash(__name__,suppress_callback_exceptions=True)
def network_graph(G, max_weight):

    # pos = nx.layout.spring_layout(G)
    # pos = nx.layout.circular_layout(G)
    # nx.layout.shell_layout only works for more than 3 nodes
    pos = nx.drawing.layout.kamada_kawai_layout(G)
    #pos = nx.drawing.layout.shell_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])


    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    ############################################################################################################################################################
    colors = list(Color('lightcoral').range_to(Color('darkred'), len(G.edges())))
    colors = ['rgb' + str(x.rgb) for x in colors]

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        weight = float(G.edges[edge]['weight']) / max_weight * 10
        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                           mode='lines',
                           line={'width': weight},
                           marker=dict(color=colors[index]),
                           line_shape='spline',
                           opacity=1)
        traceRecode.append(trace)
        index = index + 1
    ###############################################################################################################################################################
    '''node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
                            hoverinfo="text", marker={'size': 20, 'color': 'LightSkyBlue'})

    index = 0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        hovertext = G.nodes[node]['count']
        text = G.nodes[node]['text']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        index = index + 1

    traceRecode.append(node_trace)'''
    
    

    index = 0
    for node in G.nodes():
        
        x, y = G.nodes[node]['pos']
        hovertext = G.nodes[node]['count']
        text = G.nodes[node]['text']
        color = G.nodes[node]['color']
        node_trace = go.Scatter(x=tuple([x]), y=tuple([y]), hovertext=tuple([hovertext]), text=tuple([text]), mode='markers+text', textposition="bottom center",
                                hoverinfo="text", marker={'size': 20, 'color': color})
        index = index + 1

        traceRecode.append(node_trace)
    ################################################################################################################################################################
    '''middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
                                    marker={'size': 20, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        hovertext = 'hover text'
        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])
        middle_hover_trace['hovertext'] += tuple([hovertext])
        index = index + 1

    traceRecode.append(middle_hover_trace)'''
    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='Interactive Transaction Visualization', showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select'
                            )}
    return figure

req = RequeteArxiv('machine+learning')
#req = Requete("")
documents = Tweet.load_documents("tweets.csv")
#documents = req.get_documents()

corpus = Corpus(documents)
corpus.build_vocab()
corpus.build_graph()
corpus.find_communities()
corpus.find_expressions()

fig = network_graph(corpus.graph, corpus.max_weight)

app.layout = html.Div( 
    style={  'display': 'grid',
             'height':'100%',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '150px 150px 4fr',
             'gap': '10px 10px',
             'background-color': '#F8F8F8'},
    children=[
    html.H1(children='Extraction de collocations',style={'height':'100%','font-family': 'Open Sans',
            'font-style': 'bold',
            'font-size': '50px',
            'text-align': 'center',
            'padding':'0px 0px'}),
    html.Div(style={'height':'100%',
            'padding':'0px 0px',
            'border-radius':'10px',
            'background-color':'white',
            'display': 'grid',
            'grid-auto-columns': '1fr',
            'text-align': 'center',
             'grid-template-rows': '1fr 1fr'},
             children=[
                 html.Div(style={},
                          children=[
                 dcc.Input(id='search',type="text",value='', placeholder="Search Content..", name="search",style={  'padding': '10px',
  'font-size': '17px',
  'border': '1px solid grey',
  'width': '50%',
  'background': '#f1f1f1'}),
                 html.Button('search', id='search button',style={'width': '200px',
  'height': '46px',
  'background-color': '#1c89ff',
  'border': 'solid 1px transparent',
  'color': '#fff',
  'font-size': '18px',
  'cursor': 'pointer',
  'font-weight': '300'}),]),
                         html.Div( 
                     style = {
                              },
                     children = [
                         html.Label('Nombre de noeuds :',style={'font-size':'15px'}),
                          html.Div(
                             style ={
                                 'width':'20%',
                                 'padding' : '23px 0px 0px 0px',
                                 },
                              children = [dcc.Slider(
                              marks={i: '{}'.format(i) for i in range(10,55,10)},
                              min=10,
                              max=50,
                              step=10,
                              value=10,
                              verticalHeight = 100,
                              updatemode='drag'
                              ),]),               ]),]
        
        ),
    html.Div(
    style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-columns': '1fr 2fr',
             'gap': '15px 15px'
        },
    children = [ 
        html.Div(
          ),
        html.Div(
        id = 'graph',
        style={
            'border-radius': '10px',
            'background-color':'#FFFFFF',
            'padding':'10px',
            'margin':'20px'
            },
        
                children=[dcc.Graph(
        id='example-graph',
        figure=fig),]
       )
    ])
])




@app.callback(
    Output('graph', 'children'),
    Input('search button', 'n_clicks'),
    State('search', 'value'),

)
def update_output(n_clicks, search_value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        #TODO 
        req = RequeteTwitter(search_value, since='2021-01-01')
        return req.get_requete()

if __name__ == '__main__':
    app.run_server(debug=True)