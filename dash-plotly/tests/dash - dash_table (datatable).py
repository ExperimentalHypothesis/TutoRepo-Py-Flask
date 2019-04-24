import dash
import dash_table
import pandas as pd
import pymysql
import dash_html_components as html
import dash_core_components as dcc
import plotly.plotly as py
import plotly.graph_objs as go


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=["long", "short", "asdfasf"],
    data=[1,2],
)


if __name__ == '__main__':
    app.run_server(debug=True)