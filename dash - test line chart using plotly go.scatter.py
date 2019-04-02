
import dash
import dash_table
import dash_html_components as html
from flask import Flask, render_template
import pymysql
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import dash_core_components as dcc
import datetime
import numpy as np

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N)+5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-5

trace0 = go.Scatter(
    x = random_x,
    y = random_y0,
    mode = 'lines',
    line = dict( color = ('rgb(22, 96, 167)'), width = 4,),
    name = 'dsfsafasf'
)
trace1 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'lines+markers',
    name = 'lines+markers'
)
trace2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'markers',
    name = 'markers'
)


data = [trace0, trace1, trace2]


app = dash.Dash(__name__ )

app.layout = dcc.Graph(
    id = "linecharts",
    figure = go.Figure(
                        data = data, 
                        layout = go.Layout(title = "something"),
                      )
    )


if __name__ == "__main__":
    app.run_server(debug = True)