import dash
from dash import dcc
from dash import html, Input, Output, State
import plotly.graph_objs as go
import networkx as nx
from colour import Color
from dash.exceptions import PreventUpdate
from requete import Requete, RequeteTwitter, RequeteArxiv, get_documents_sample
from corpus import Corpus
import pandas as pd
from dash import dash_table

app = dash.Dash(__name__,suppress_callback_exceptions=True)
def network_graph(G, max_weight):

    #pos = nx.drawing.layout.kamada_kawai_layout(G)
    pos = nx.drawing.layout.shell_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])


    traceRecode = []  # contains edge_trace, node_trace, middle_node_trace
    
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


documents = get_documents_sample()

corpus = Corpus(documents)
corpus.build_vocab()
corpus.build_graph()
corpus.find_communities()
fig = network_graph(corpus.graph, corpus.max_weight)

expressions = corpus.find_expressions()

df = pd.DataFrame (expressions, columns = ['Les expression courantes :'])
data = df.to_dict('records')

app.layout = html.Div( 
    style={  'display': 'grid',
             'height':'100%',
             'grid-auto-columns': '1fr',
             'grid-template-rows': '70px 100px 4fr',
             'gap': '10px 10px',
             'background-color': '#F8F8F8'},
    children=[
    html.H1(children='Extraction de collocations',style={'height':'80%','font-family': 'Open Sans',
            'font-style': 'bold',
            'font-size': '30px',
            'text-align': 'center',
            'margin':'20px'}),
    html.Div(style={'height':'100%',
            'padding':'0px 0px',
            'margin':'0px 20px',
            'border-radius':'10px',
            'background-color':'white',
            'display': 'grid',
            'grid-auto-columns': '1fr',
             'grid-template-columns': '1fr 4fr 1fr '},
             children=[
                 dcc.RadioItems(
                 id = 'extraction',
                  style={'padding':'25px 30px'},
                  options=[
                      {'label': 'Tweeter', 'value': 'twitter'},
                      {'label': 'Arxiv', 'value': 'arxiv'}
                    ],
                  value='twitter',
                  labelStyle={'display': 'block'}
                 ),
                 html.Div(style={'padding':'25px'},
                          children=[
                 dcc.Input(id='search',type="text",value='', placeholder="Search Content..", name="search",style={  'padding': '10px',
  'font-size': '17px',
  'border': '1px solid grey',
  'width': '65%',
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
                     style = { 'padding':'25px 0px'
                              },
                     children = [
                         html.Label('Nombre de noeuds :',style={'height':'100%','width':'100%','font-size':'15px'}),
                          html.Div(
                             style ={'padding':'5px 0px '
                                 },
                              children = [dcc.Slider(
                              id='slider',
                              marks={i: '{}'.format(i) for i in range(10,55,10)},
                              min=10,
                              max=50,
                              step=10,
                              value=20,
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
         
              style={
            'border-radius': '10px',
            'background-color':'#FFFFFF',
            'padding':'10px',
            'margin':'20px'
            },
              children=[
                  dash_table.DataTable(
                         id = 'list',
                         style_cell={'textAlign': 'left',
                                     'font-family': 'Open Sans',
                                     'font-style': 'regular',
                                     'font-size': '17px',
                                     'height':'50px',
                                     'padding':'0px 10px'},
                             style_header={
        'backgroundColor': '#F8F8F8',
        'color': '#123456',
        'fontWeight': 'bold'
    },
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
)
                  ]
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
    Output('example-graph', 'figure'),
    Output('list','data'),
    Input('search button', 'n_clicks'),
    Input('slider', 'value'),
    State('search', 'value'),
    State('extraction','value')

)
def update_output(n_clicks,slider_value,search_value,extraction_value):
    ctx = dash.callback_context
    if ctx.triggered:
       trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
       if (trigger_id =="search button"):
        if n_clicks is None:
          raise PreventUpdate
        else:
        #TODO 
           
           if extraction_value == 'twitter':
               req = RequeteTwitter(search_value)
           else:
               req = RequeteArxiv(search_value)
           
           try:
               documents = req.get_documents()
           except:
               documents = get_documents_sample()
           
           global corpus
           global data
           
           corpus = Corpus(documents)
           corpus.build_vocab()
           corpus.build_graph(slider_value)
           corpus.find_communities()
           figure = network_graph(corpus.graph, corpus.max_weight)
           
           expressions = corpus.find_expressions()
           df = pd.DataFrame (expressions, columns = ['Les expression courantes :'])
           data = df.to_dict('records')
           
           return figure, data
       else:
           
           corpus.build_graph(max_nodes=slider_value)
           corpus.find_communities()
           figure = network_graph(corpus.graph, corpus.max_weight)
           
           return figure, data
    else: return fig ,None


if __name__ == '__main__':
    app.run_server(debug=True)
