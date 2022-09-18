from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import model
from datetime import datetime
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

app = Dash(__name__)
app.title = "STORIES"

model = model.DashModel()

f = go.Figure()
f.add_trace(go.Scatter(x=[0,3], y=[0,5]))
f.update_layout(legend_title_text='Original source', legend=dict(orientation="v", traceorder='reversed', font_size=16, bgcolor='#585858'))
f.update_layout(paper_bgcolor='#585858', plot_bgcolor='#585858')
f.update_xaxes(showline=True, linewidth=2, linecolor="#999", gridcolor='#ff7b3e', color='#ff7b3e', zerolinecolor='#ff7b3e')
f.update_yaxes(showline=True, linewidth=2, linecolor="#999", gridcolor='#ff7b3e', color='#ff7b3e', zerolinecolor='#ff7b3e')

divs = []
clicks = 0
divs.append(html.Div([
        html.H1(children='Analysis of the development of plots', className="header-title") 
    ]))

divs.append(html.P(children="Set the parameters and click refresh graph. It takes time to update", id='comment',
                    className="lead",))

divs.append(html.Button(children = 'Update', id='refresh-data', n_clicks=0, className="btn btn-outline-primary"))
divs.append(html.Div(children=' ', id='last-update')) 

divs.append(html.Div([dcc.Input(id='slice', placeholder='amount of data', type='number', className="form-control"), 
        dcc.Input(id='mounth', placeholder='month number', type='number', className="form-control"),
        dcc.Input(id='coef', placeholder='similarity coefficient', type='number', className="form-control"),
        dcc.Input(id='min', placeholder='min chain length', type='number', className="form-control"),
        dcc.Input(id='max', placeholder='max chain length', type='number', className="form-control")]))

divs.append(html.Div([
    html.A(children='Select an element to get a link', 
        id='link',
        href='', 
        target='_blank',
        className="btn btn-outline-primary"),

    dcc.Graph(
        id='graph',
        figure=f,
        className="card-body",
    ),  
]))

#style={'width': '80vh', 'height': '10vh'}
@app.callback(
    Output('link', 'href'),
    [Input('graph', 'clickData')])
def change_click_data(clickData):
    if clickData:
        target = clickData['points'][0]['customdata']
        return target
    else:
        raise PreventUpdate

@app.callback(
    Output('link', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData:
        target = clickData['points'][0]['customdata']
        return target
    else:
        raise PreventUpdate

@app.callback(
    Output('graph', 'figure'), Output('refresh-data', 'children'), Output('refresh-data', 'n_clicks'),
    [Input('slice', 'value'), Input('mounth', 'value'), Input('coef', 'value'), Input('min', 'value'), Input('max', 'value'), Input('refresh-data', 'n_clicks')])
def display_click_data(*vals):
    global f
    global model
    global clicks
    print(vals)
    print(clicks) 
    if clicks == vals[5] or vals[0] == None or vals[1] == None or vals[2] == None or vals[3] == None or vals[4] == None:
        update = 'Update                (last update: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' )'
        return f, update, clicks 
    else:
        data = model.simlarFil(model.get_data(vals[0], vals[1], 2022), vals[2], vals[3], vals[4])
        f = model.ploting(data[0], data[1])
        update = 'Update                (last update: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' )'
        clicks += 1
        return f, update, clicks

app.layout = html.Div(children=divs)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)



