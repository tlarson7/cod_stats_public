from dash import Dash
from layout import layout, get_callbacks

app = Dash(__name__)
server = app.server
app.layout = layout
get_callbacks(app)
app.title = "Hayz Stats v0.1"

# app.run_server(host='0.0.0.0', port='8050')
app.run_server(port='8050')
# app.run_server()
# http://23.127.68.202:8050/