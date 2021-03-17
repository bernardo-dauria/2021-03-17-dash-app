import dash

from dash.dependencies import Input, Output, State



import dash_html_components as html

import dash_core_components as dcc

import dash_table as dt



import pandas as pd

import plotly.express as px

df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url).dropna(subset=['vore'])



df_cols = [{"name": i, "id": i} for i in df.columns]

df_vore = df['vore'].sort_values().unique()

opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

col_vore = {x:px.colors.qualitative.Pastel[i] for i, x in enumerate(df_vore)}



print(col_vore)



app = dash.Dash(__name__, title="Dash App")





markdown_text = '''

## Some references

- [Dash HTML Components](dash.plotly.com/dash-html-components)

- [Dash Core Components](dash.plotly.com/dash-core-components)  

- [Dash Bootstrap Components](dash-bootstrap-components.opensource.faculty.ai/docs/components)  

'''

table_tab = dt.DataTable(id="my-table",

                columns = df_cols,

                data= df.to_dict("records")

            )

graph_tab = dcc.Graph(id="my_graph",

                figure= px.scatter(df,

                    x="bodywt",

                    y="sleep_total",

                    color="vore",

                    color_discrete_map= col_vore)

            )



app.layout = html.Div([

    html.Div([

        html.H1(app.title, className= "app-header--title")

    ], className= "app-header"),

    html.Div([
        dcc.Markdown(markdown_text),
        html.Label(["Select types of feeding strategies:",
            dcc.Dropdown('my-dropdown',
                options= opt_vore,
                value= [df_vore[0]],
                multi= True
            )
        ]),
        dcc.Slider(
            min=-5,
            max=10,
            step=0.5,
            value=-3
        ),
        dcc.Tabs(id="tabs", value='tab-t', children=[

            dcc.Tab(label='Table', value='tab-t'),

            dcc.Tab(label='Graph', value='tab-g'),

        ]),

        html.Div(id="tabs-content")

    ], className = "app-body")

])





@app.callback(

     Output('my-table', 'data'),

     Input('my-dropdown', 'value'))

def update_data(values):

    filter = df['vore'].isin(values)

    return df[filter].to_dict("records")



@app.callback(

     Output('my_graph', 'figure'),

     Input('my-dropdown', 'value'))

def update_figure(values):

    filter = df['vore'].isin(values)

    return px.scatter(df[filter], x="bodywt", y="sleep_total", color="vore", color_discrete_map= col_vore)



@app.callback(

     Output('tabs-content', 'children'),

     Input('tabs', 'value'))

def update_tabs(v):

    if v == 'tab-g':

        return graph_tab

    return table_tab



if __name__ == '__main__':
    # app.server.run(debug=True)
    app.server.run(debug=True, port=5858,  host='minivideos.uc3m.es')