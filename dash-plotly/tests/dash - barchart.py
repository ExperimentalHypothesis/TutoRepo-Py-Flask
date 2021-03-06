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
import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Bar(
    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
       350, 430, 474, 526, 488, 537, 500, 439],
    name='Rest of world',
    marker=dict(
        color='rgb(55, 83, 109)'
    )
)
trace2 = go.Bar(
    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
    y=[16, 13, 10, 11, 28, 37, 43, 55, -56, 88, 105, 156, 270,
       299, 340, 403, 549, 499],
    name='China',
    marker=dict(
        color='rgb(26, 118, 255)'
    )
)
data = [trace1, trace2]

layout = go.Layout(
    title='US Export of Plastic Scrap',
    xaxis=dict(
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='USD (millions)',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1
)

app = dash.Dash(__name__)

app.layout = dcc.Graph(
    id = "barchart",
    figure = go.Figure(
                        data = data,
                        layout = layout
                       )
    
    )


if __name__ == "__main__":
    app.run_server(debug=True)