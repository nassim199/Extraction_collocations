from datetime import date
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import networkx as nx
from colour import Color

from requete import Requete
from document import Tweet
from corpus import Corpus

app = dash.Dash(__name__)

def network_graph(G, max_weight):

    # pos = nx.layout.spring_layout(G)
    # pos = nx.layout.circular_layout(G)
    # nx.layout.shell_layout only works for more than 3 nodes
    pos = nx.drawing.layout.spring_layout(G)
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
    node_trace = go.Scatter(x=[], y=[], hovertext=[], text=[], mode='markers+text', textposition="bottom center",
                            hoverinfo="text", marker={'size': 50, 'color': 'LightSkyBlue'})

    index = 0
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        hovertext = str(node)
        text = 'text'
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        index = index + 1

    traceRecode.append(node_trace)
    ################################################################################################################################################################
    middle_hover_trace = go.Scatter(x=[], y=[], hovertext=[], mode='markers', hoverinfo="text",
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

    traceRecode.append(middle_hover_trace)
    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='Interactive Transaction Visualization', showlegend=False, hovermode='closest',
                            margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select',
                            annotations=[
                                dict(
                                    ax=(G.nodes[edge[0]]['pos'][0] + G.nodes[edge[1]]['pos'][0]) / 2,
                                    ay=(G.nodes[edge[0]]['pos'][1] + G.nodes[edge[1]]['pos'][1]) / 2, axref='x', ayref='y',
                                    x=(G.nodes[edge[1]]['pos'][0] * 3 + G.nodes[edge[0]]['pos'][0]) / 4,
                                    y=(G.nodes[edge[1]]['pos'][1] * 3 + G.nodes[edge[0]]['pos'][1]) / 4, xref='x', yref='y',
                                    showarrow=True,
                                    arrowhead=3,
                                    arrowsize=4,
                                    arrowwidth=1,
                                    opacity=1
                                ) for edge in G.edges]
                            )}
    return figure

req = Requete('santiago-de-compostela', since='2022-01-01')
tweets = Tweet.get_tweets(req)

corpus = Corpus(tweets)
corpus.build_vocab()
corpus.build_graph()

fig = network_graph(corpus.graph, corpus.max_weight)

app.layout = html.Div( 
    style={  'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '1fr 4fr',
             'gap': '10px 10px'},
    children=[
    html.H1(children='Hello Dash'),

    html.Div(
    style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-columns': '1fr 2fr',
             'gap': '10px 10px'
        },
    children = [ 
        
        html.Div(
            style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '1fr 1fr 1fr 1fr 1fr',
             'gap': '30px 30px',
             'padding': '0px 0px 0px 15px'
                },
            children=[
                 html.Div(children=[
                    html.Label('Language : '),
                    dcc.Dropdown(
                     options=[
                           {'value':'ar','label':'Arabic (العربية)'},
                           {'value':'de','label':'German (Deutsch)'},
                           {'value':'en','label':'English (English)'},
                           {'value':'es','label':'Spanish (Español)'},
                           {'value':'fr','label': 'French (Français)'},
                           {'value':'hi','label': 'Hindi (हिंदी)'},
                           {'value':'it','label': 'Italian (Italiano)'},
                           {'value':'ja','label': 'Japanese (日本語)'},
                           {'value':'nl','label':'Dutch (Nederlands)'},
                           {'value':'pt','label':'Portuguese (Português)'},
                           {'value':'ru','label':'Russian (Русский)'},
                           {'value':'tr','label':'Turkish (Türkçe)'},
                           {'value':'zh','label':'Chinese (中文)'}
                           ],
                     value=''
                    ),]),
                 html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('Content :'),
                    dcc.Input(value='', type='text',placeholder='Content',style={'height':'70%','width':'100%' }),
                ]),
                     html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('User :'),
                    dcc.Input(value='', type='text',placeholder='User',style={'height':'70%','width':'100%' }),
                ]),
                   html.Div( 
                      style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-columns': '1fr 1fr',
             'gap': '10px 10px'
                       },
                      children = [
                            html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('Location :'),
                    dcc.Input(value='', type='text',placeholder='Location',style={'height':'70%','width':'100%' }),
                ]),
                html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('Zone en Km :',style={'padding': '0px 0px 0px 15px'}),
                         html.Div(
                             style ={
                                 'padding' : '13px 0px 0px 0px'
                                 },
                              children = [dcc.Slider(
                              marks={i: '{}'.format(i) for i in range(5,55,5)},
                              min=5,
                              max=50,
                              step=5,
                              value=5,
                              updatemode='drag'
                              ), ]),               ]),
    
                          ]
        
        ),
            
                  dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2017, 9, 19),
        initial_visible_month=date(2017, 8, 5),
        end_date=date(2017, 8, 25)),
                   ]),
        dcc.Graph(
        id='example-graph',
        figure=fig),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)