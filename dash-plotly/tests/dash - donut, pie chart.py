
import dash
import dash_table
import pandas as pd
import pymysql
import dash_html_components as html
import dash_core_components as dcc
import plotly.plotly as py
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = dcc.Graph(
            id='donut',
            figure = {
                        "data": [
                        {
                            "values": [16, 15, 12, 6, 5, 4, 42],
                            "labels": [
                                        "US",
                                        "China",
                                        "European Union",
                                        "Russian Federation",
                                        "Brazil",
                                        "India",
                                        "Rest of World"
                                        ],
                            "domain": {"x": [0, .48]},
                            "name": "GHG Emissions",
                            "hoverinfo":"label+percent+name",
                            "hole": .4,
                            "type": "pie"
                        },
    ],
  "layout": { "title":"Global Emissions 1990-2011"})





if __name__ == '__main__':
    app.run_server(debug=True)