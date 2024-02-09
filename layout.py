import dash
from dash import dash_table, html, dcc, Output, Input
import pandas as pd

df = pd.read_csv('final_stats.csv')

table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], sort_action="native")

dropdown_text = html.H2('Use dropdown below to select player')
dropdown_options = df['player']
dropdown = dcc.Dropdown(dropdown_options, id='Player Dropdown')

tab1_content = html.Div(children=[dropdown_text, dropdown, table], id='main')
tab1 = dcc.Tab(children=[tab1_content], label='All games')


table2 = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], sort_action="native")
# dropdown_text = html.H2('Use dropdown below to select player')
# dropdown_options = df['player']
dropdown2 = dcc.Dropdown(dropdown_options, id='Player Dropdown 2')

table_div = html.Div(children=[table2], id='Totals Table')
tab2_content = html.Div(children=[dropdown_text, dropdown2, table_div], id='tab2')
tab2 = dcc.Tab(children=[tab2_content], label='Totals per player')

tabs = dcc.Tabs(children=[tab1, tab2])

layout = html.Div(children=[tabs])


def create_table(df):
    table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                 sort_action="native")
    return table


def get_callbacks(app):

    @app.callback(
        Output('main', 'children'),
        Input('Player Dropdown', 'value')
    )
    def update_df(val):
        new_df = df.copy()
        new_df.query('player == @val', inplace=True)

        new_table = dash_table.DataTable(new_df.to_dict('records'), [{"name": i, "id": i} for i in new_df.columns],
                                     sort_action="native")
        return [dropdown_text, dropdown, new_table]


    @app.callback(
        Output('Totals Table', 'children'),
        Input('Player Dropdown 2', 'value')
    )
    def update_totals(player):
        if player is None:
            return dash.no_update
        new_df = df.copy()
        new_df.query('player == @player', inplace=True)
        new_df = new_df[['player', 'score', 'kills', 'deaths', 'time', 'defends']]

        new_df[['min', 'sec']] = new_df['time'].str.split(':', expand=True)
        new_df['min'] = pd.to_numeric(new_df['min'])
        new_df['sec'] = pd.to_numeric(new_df['sec'])
        new_df['ht_num'] = new_df['min'] * 60 + new_df['sec']
        new_df = new_df[['player', 'score', 'kills', 'deaths', 'ht_num', 'defends']]

        final_df = new_df.groupby('player').sum()
        final_df['KD'] = round(final_df['kills'] / final_df['deaths'], 2)
        final_df['min'] = final_df['ht_num'] // 60
        final_df['min'] = final_df['min'].astype(str)
        final_df['sec'] = final_df['ht_num'] % 60
        final_df['sec'] = final_df['sec'].astype(str)
        final_df['time'] = final_df['min'] + ':' + final_df['sec']
        final_df = final_df[['score', 'kills', 'deaths', 'KD', 'time', 'defends']]

        return [create_table(final_df)]
