from dash import Dash
from dash import dash_table, html, dcc, Output, Input
import pandas as pd
# from layout import layout, get_callbacks

app = Dash(__name__)
server = app.server

# layout = html.Div([html.Header('test')])
df = pd.read_csv('https://raw.githubusercontent.com/tlarson7/public_cod_stats_raw_data/main/final_stats.csv')
table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], sort_action="native")
layout = html.Div([table])

app.layout = layout
# get_callbacks(app)
app.title = "Hayz Stats v0.1"

# app.run_server(host='0.0.0.0', port='8050')
# app.run_server(port='8050')
# app.run_server(debug=False)
app.run_server(host='0.0.0.0', port='10000')
# http://23.127.68.202:8050/
