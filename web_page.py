from datetime import date
import dash
from dash import dcc
from dash import html, Input, Output, State
import plotly.graph_objs as go
import networkx as nx
from colour import Color

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

fig = network_graph(corpus.graph, corpus.max_weight)

app.layout = html.Div( 
    style={  'display': 'grid',
             'height':'100%',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '150px 4fr',
             'gap': '10px 10px',
             'background-color': '#F8F8F8'},
    children=[
    html.H1(children='Extraction de collocations',style={'height':'100%','font-family': 'Open Sans',
            'font-style': 'bold',
            'font-size': '50px',
            'text-align': 'center',
            'padding':'0px 0px'}),

    html.Div(
    style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-columns': '1fr 2fr',
             'gap': '15px 15px'
        },
    children = [ 
        html.Div(
          children=[ dcc.Tabs(id="Tab", value='Tweeter_Tab', children=[
        dcc.Tab(label='Tweeter', value='Tweeter_Tab'),
        dcc.Tab(label='Arxiv', value='Arxiv_Tab'),
    ]),

    html.Div(id='Content')]
            ),
        html.Div(
        style={
            'border-radius': '10px',
            'background-color':'#FFFFFF',
            'padding':'10px',
            'margin':'20px'
            },
        
        children=[dcc.Graph(
        id='example-graph',
        figure=fig),])
    ])
])



@app.callback(Output('Content', 'children'),
              Input('Tab', 'value'))
def render_content(tab):
    if tab == 'Tweeter_Tab':
        return html.Div(
            style = {'display': 'grid',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '1fr 1fr 1fr 1fr 1fr 1fr',
             'gap': '30px 30px',
             'background-color':'#FFFFFF',
             'border-radius': '10px',
             'padding': '20px 10px 0px 15px',
             'margin':'20px'
                },
            children=[
                 html.Div(children=[
                    html.Label('Language : '),
                    dcc.Dropdown(
                     style = {
                         'padding':'10px'
                         },
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
                         html.Div(
                         style={'padding':'10px','height':'50%'},
                         children = [dcc.Input(id='search', value='', type='text',placeholder='Content',style={'height':'100%','width':'98%'})
                                     ]),
                ]),
                     html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('User :'),
                         html.Div(
                         style={'padding':'10px','height':'50%'},
                         children = [dcc.Input(id='user', value='', type='text',placeholder='User',style={'height':'100%','width':'98%'})
                                     ]),
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
                        html.Div(
                         style={'padding':'10px','height':'50%'},
                         children = [dcc.Input(value='', type='text',placeholder='Location',style={'height':'100%','width':'98%'})
                                     ]),
                ]),
                html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('Zone en Km :',style={'padding': '0px 0px 0px 15px'}),
                         html.Div(
                             style ={
                                 'padding' : '23px 0px 0px 0px',
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
           html.Div( 
                     style = {'height':'100%',
                              'width' : '100%'},
                     children = [
                         html.Label('Date :'),
                         html.Div(
                         style={'padding':'10px','height':'50%'},
                         children = [dcc.DatePickerRange(
                             style={'height':'100%','width':'98%'},
        id='date-picker-range',
        end_date_placeholder_text='Select a date!'   )                                 ]),
                         ]),  
            
            html.Div(
                style = {'display': 'grid',
       'grid-auto-columns': '1fr',
       'grid-template-columns': '1fr 1fr',
       'gap': '10px 10px'
                 },
                children = [
                        html.Div(id='requete', children='requete'),
                        html.Button('search', id='search-button',style={'width': '200px',
  'height': '46px',
  'border-radius': '18px',
  'background-color': '#1c89ff',
  'border': 'solid 1px transparent',
  'color': '#fff',
  'font-size': '18px',
  'cursor': 'pointer',
  'font-weight': '300'})
                    ]
                ),
                   ]),
    elif tab == 'Arxiv_Tab':
        return html.Div([
            html.H3('Tab content Arxiv'),
            #To Do implementation
        ])
@app.callback(
    Output('requete', 'children'),
    Input('search-button', 'n_clicks'),
    State('search', 'value'),
    State('user', 'value'),
    suppress_callback_exceptions=True,

)
def update_output(n_clicks, search_value, user_value):
    req = RequeteTwitter(search_value, user=user_value, since='2021-01-01')
    
    return req.get_requete()

if __name__ == '__main__':
    app.run_server(debug=True)